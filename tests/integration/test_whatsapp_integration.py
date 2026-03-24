"""
Integration tests for the WhatsApp webhook endpoint.

These tests make REAL API calls to OpenAI, Groq, ElevenLabs, and Together AI.
Only WhatsApp network I/O is mocked (media download/upload and message sending).

Run in isolation to avoid module caching conflicts with unit tests:
    pytest tests/integration/ -v
"""
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

ASSETS_DIR = Path(__file__).parent.parent.parent / "assets"


# --- Payload helpers (same structure as real WhatsApp Cloud API) ---

def _text_payload(body: str = "Hello! What is your name?", from_number: str = "1234567890") -> dict:
    return {
        "entry": [{"changes": [{"value": {
            "messages": [{"from": from_number, "type": "text", "text": {"body": body}}]
        }}]}]
    }


def _audio_payload(from_number: str = "1234567890", media_id: str = "audio-001") -> dict:
    return {
        "entry": [{"changes": [{"value": {
            "messages": [{"from": from_number, "type": "audio", "audio": {"id": media_id}}]
        }}]}]
    }


def _image_payload(caption: str = "What do you see?", from_number: str = "1234567890") -> dict:
    return {
        "entry": [{"changes": [{"value": {
            "messages": [{
                "from": from_number,
                "type": "image",
                "image": {"id": "img-001", "caption": caption},
            }]
        }}]}]
    }


# --- Tests ---

@pytest.mark.asyncio
@pytest.mark.integration
async def test_text_message_real_llm(client):
    """Full graph run with a real LLM call. Asserts a non-empty text response is sent."""
    captured = {}

    async def capture_send(from_number, response_text, message_type="text", media_content=None):
        captured["response_text"] = response_text
        captured["message_type"] = message_type
        return True

    with patch("interfaces.whatsapp.whatsapp_response.send_response", side_effect=capture_send):
        response = await client.post("/whatsapp_response", json=_text_payload())

    assert response.status_code == 200
    assert captured["message_type"] == "text"
    assert len(captured["response_text"]) > 0
    print(f"\n[LLM response] {captured['response_text']}")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_audio_message_real_stt_and_tts(client, audio_bytes):
    """
    Uses real assets/recording_asking_time.mp3.
    Groq Whisper transcribes it, the graph generates a response,
    ElevenLabs synthesizes audio. Asserts audio bytes are returned.
    """
    captured = {}

    async def capture_send(from_number, response_text, message_type="text", media_content=None):
        captured["response_text"] = response_text
        captured["message_type"] = message_type
        captured["audio_bytes"] = media_content
        return True

    async def fake_process_audio(message):
        """Download is mocked — transcribe the real asset file instead."""
        from interfaces.whatsapp.whatsapp_response import speech_to_text
        return await speech_to_text.transcribe(audio_bytes)

    with (
        patch("interfaces.whatsapp.whatsapp_response.process_audio_message", side_effect=fake_process_audio),
        patch("interfaces.whatsapp.whatsapp_response.send_response", side_effect=capture_send),
    ):
        response = await client.post("/whatsapp_response", json=_audio_payload())

    assert response.status_code == 200
    assert captured["message_type"] == "text"
    assert isinstance(captured["audio_bytes"], bytes) and len(captured["audio_bytes"]) > 0
    print(f"\n[Transcription → LLM response] {captured['response_text']}")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_image_message_real_vision(client, image_bytes):
    """
    Uses real assets/download.jpeg.
    OpenAI vision analyzes it, the graph generates a response.
    Asserts a non-empty text or image response is returned.
    """
    captured = {}

    async def capture_send(from_number, response_text, message_type="text", media_content=None):
        captured["response_text"] = response_text
        captured["message_type"] = message_type
        return True

    with (
        patch(
            "interfaces.whatsapp.whatsapp_response.download_media",
            new_callable=AsyncMock,
            return_value=image_bytes,
        ),
        patch("interfaces.whatsapp.whatsapp_response.send_response", side_effect=capture_send),
        patch("interfaces.whatsapp.whatsapp_response.upload_media", new_callable=AsyncMock, return_value="mock-media-id"),
    ):
        response = await client.post(
            "/whatsapp_response",
            json=_image_payload(caption="What do you see in this image?"),
        )

    assert response.status_code == 200
    assert len(captured.get("response_text", "")) > 0
    print(f"\n[Vision → LLM response] {captured['response_text']}")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_image_generation_real_together_ai(client):
    """
    User explicitly requests an image. The router routes to image_node,
    which calls Together AI (FLUX.1-schnell) to generate one.
    Asserts an image file is created and sent back.
    """
    captured = {}

    async def capture_send(from_number, response_text, message_type="text", media_content=None):
        captured["response_text"] = response_text
        captured["message_type"] = message_type
        captured["image_bytes"] = media_content
        return True

    with (
        patch("interfaces.whatsapp.whatsapp_response.send_response", side_effect=capture_send),
        patch("interfaces.whatsapp.whatsapp_response.upload_media", new_callable=AsyncMock, return_value="mock-media-id"),
    ):
        response = await client.post(
            "/whatsapp_response",
            json=_text_payload(body="Can you send me an image of a mountain landscape at sunset?"),
        )

    assert response.status_code == 200
    assert captured["message_type"] == "image"
    assert isinstance(captured["image_bytes"], bytes) and len(captured["image_bytes"]) > 0
    print(f"\n[Image gen response] {captured['response_text']}")
