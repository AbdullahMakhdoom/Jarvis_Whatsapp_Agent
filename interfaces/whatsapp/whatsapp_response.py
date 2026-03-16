import logging
import os
from io import BytesIO
from typing import Set
import httpx
from fastapi import APIRouter, BackgroundTasks, Request, Response
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from src.graph import create_workflow_graph
from src.modules.image.image_to_text import ImageToText
from src.modules.speech.speech_to_text import SpeechToText
from src.modules.speech.text_to_speech import TextToSpeech
from src.settings import settings
from .models import WhatsAppMessage, WhatsAppWebhookPayload

logger = logging.getLogger(__name__)

# Global module instances
speech_to_text = SpeechToText()
text_to_speech = TextToSpeech()
image_to_text = ImageToText()

# Router for WhatsApp respo
whatsapp_router = APIRouter()

# Deduplication set for processed message IDs
_processed_message_ids: Set[str] = set()

# WhatsApp API credentials
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")


@whatsapp_router.get("/whatsapp_response")
async def whatsapp_verify(request: Request) -> Response:
    """Handles WhatsApp webhook verification."""
    params = request.query_params
    if params.get("hub.verify_token") == os.getenv("WHATSAPP_VERIFY_TOKEN"):
        return Response(content=params.get("hub.challenge"), status_code=200)
    return Response(content="Verification token mismatch", status_code=403)


@whatsapp_router.post("/whatsapp_response")
async def whatsapp_handler(payload: WhatsAppWebhookPayload, background_tasks: BackgroundTasks) -> Response:
    """Handles incoming messages and status updates from the WhatsApp Cloud API."""
    try:
        change_value = payload.entry[0].changes[0].value
        if change_value.messages:
            message = change_value.messages[0]

            logger.info(f"Incoming message id={message.id!r} from={message.from_!r} type={message.type!r}")

            # Deduplicate: skip if already processed
            if message.id and message.id in _processed_message_ids:
                logger.info(f"Duplicate message {message.id} ignored")
                return Response(content="OK", status_code=200)

            if message.id:
                _processed_message_ids.add(message.id)

            background_tasks.add_task(process_and_reply, message)
            return Response(content="OK", status_code=200)

        elif change_value.statuses:
            return Response(content="OK", status_code=200)

        else:
            return Response(content="OK", status_code=200)

    except Exception as e:
        logger.error(f"Error handling webhook: {e}", exc_info=True)
        return Response(content="OK", status_code=200)


async def process_and_reply(message: WhatsAppMessage) -> None:
    """Process the message through the AI graph and send the reply."""
    try:
        from_number = message.from_
        session_id = from_number

        # Get user message and handle different message types
        content = ""
        if message.type == "audio":
            content = await process_audio_message(message)
        elif message.type == "image":
            content = message.image.caption or "" if message.image else ""
            image_bytes = await download_media(message.image.id)
            try:
                description = await image_to_text.analyze_image(
                    image_bytes,
                    "Please describe what you see in this image in the context of our conversation.",
                )
                content += f"\n[Image Analysis: {description}]"
            except Exception as e:
                logger.warning(f"Failed to analyze image: {e}")
        else:
            content = message.text.body

        # Process message through the graph agent
        async with AsyncSqliteSaver.from_conn_string(settings.SHORT_TERM_MEMORY_DB_PATH) as short_term_memory:
            graph = create_workflow_graph().compile(checkpointer=short_term_memory)
            await graph.ainvoke(
                {"messages": [HumanMessage(content=content)]},
                {"configurable": {"thread_id": session_id}},
            )
            output_state = await graph.aget_state(config={"configurable": {"thread_id": session_id}})

        workflow = output_state.values.get("workflow", "conversation")
        response_message = output_state.values["messages"][-1].content

        if workflow == "audio":
            audio_buffer = output_state.values["audio_buffer"]
            await send_response(from_number, response_message, "audio", audio_buffer)
        elif workflow == "image":
            image_path = output_state.values["image_path"]
            with open(image_path, "rb") as f:
                image_data = f.read()
            await send_response(from_number, response_message, "image", image_data)
        else:
            await send_response(from_number, response_message, "text")

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)


async def download_media(media_id: str) -> bytes:
    """Download media from WhatsApp."""
    media_metadata_url = f"https://graph.facebook.com/v21.0/{media_id}"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}

    async with httpx.AsyncClient() as client:
        metadata_response = await client.get(media_metadata_url, headers=headers)
        metadata_response.raise_for_status()
        metadata = metadata_response.json()
        download_url = metadata.get("url")

        media_response = await client.get(download_url, headers=headers)
        media_response.raise_for_status()
        return media_response.content


async def process_audio_message(message: WhatsAppMessage) -> str:
    """Download and transcribe audio message."""
    audio_id = message.audio.id
    media_metadata_url = f"https://graph.facebook.com/v21.0/{audio_id}"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}

    async with httpx.AsyncClient() as client:
        metadata_response = await client.get(media_metadata_url, headers=headers)
        metadata_response.raise_for_status()
        metadata = metadata_response.json()
        download_url = metadata.get("url")

    # Download the audio file
    async with httpx.AsyncClient() as client:
        audio_response = await client.get(download_url, headers=headers)
        audio_response.raise_for_status()

    # Prepare for transcription
    audio_buffer = BytesIO(audio_response.content)
    audio_buffer.seek(0)
    audio_data = audio_buffer.read()

    return await speech_to_text.transcribe(audio_data)


async def send_response(
    from_number: str,
    response_text: str,
    message_type: str = "text",
    media_content: bytes = None,
) -> bool:
    """Send response to user via WhatsApp API."""
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    if message_type in ["audio", "image"]:
        try:
            mime_type = "audio/mpeg" if message_type == "audio" else "image/png"
            media_buffer = BytesIO(media_content)
            media_id = await upload_media(media_buffer, mime_type)
            json_data = {
                "messaging_product": "whatsapp",
                "to": from_number,
                "type": message_type,
                message_type: {"id": media_id},
            }

            # Add caption for images
            if message_type == "image":
                json_data["image"]["caption"] = response_text
        except Exception as e:
            logger.error(f"Media upload failed, falling back to text: {e}")
            message_type = "text"

    if message_type == "text":
        json_data = {
            "messaging_product": "whatsapp",
            "to": from_number,
            "type": "text",
            "text": {"body": response_text},
        }

    print(headers)
    print(json_data)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_NUMBER_ID}/messages",
            headers=headers,
            json=json_data,
        )

    return response.status_code == 200


async def upload_media(media_content: BytesIO, mime_type: str) -> str:
    """Upload media to WhatsApp servers."""
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    files = {"file": ("response.mp3", media_content, mime_type)}
    data = {"messaging_product": "whatsapp", "type": mime_type}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_NUMBER_ID}/media",
            headers=headers,
            files=files,
            data=data,
        )
        result = response.json()

    if "id" not in result:
        raise Exception("Failed to upload media")
    return result["id"]