from typing import List, Optional

from pydantic import BaseModel, Field


class WhatsAppText(BaseModel):
    body: str


class WhatsAppImage(BaseModel):
    id: str
    caption: Optional[str] = None


class WhatsAppAudio(BaseModel):
    id: str


class WhatsAppMessage(BaseModel):
    model_config = {"populate_by_name": True}

    id: Optional[str] = None
    from_: str = Field(alias="from")
    type: str
    text: Optional[WhatsAppText] = None
    image: Optional[WhatsAppImage] = None
    audio: Optional[WhatsAppAudio] = None


class WhatsAppChangeValue(BaseModel):
    messages: Optional[List[WhatsAppMessage]] = None
    statuses: Optional[List[dict]] = None


class WhatsAppChange(BaseModel):
    value: WhatsAppChangeValue


class WhatsAppEntry(BaseModel):
    changes: List[WhatsAppChange]


class WhatsAppWebhookPayload(BaseModel):
    entry: List[WhatsAppEntry]
