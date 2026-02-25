import os
import wave
from io import BytesIO
from typing import Optional

from ...exceptions import SpeechToTextError
from ...settings import settings
from groq import Groq


class SpeechToText:
    """A class to handle speech-to-text conversion using Groq's Whisper model."""

    # Required environment variables
    REQUIRED_ENV_VARS = ["GROQ_API_KEY"]

    def __init__(self):
        """Initialize the SpeechToText class and validate environment variables."""
        self._validate_env_vars()
        self._client: Optional[Groq] = None

    def _validate_env_vars(self) -> None:
        """Validate that all required environment variables are set."""
        missing_vars = [var for var in self.REQUIRED_ENV_VARS if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    @property
    def client(self) -> Groq:
        """Get or create Groq client instance using singleton pattern."""
        if self._client is None:
            self._client = Groq(api_key=settings.GROQ_API_KEY)
        return self._client

    async def transcribe(self, audio_data: bytes) -> str:
        """Convert speech to text using Groq's Whisper model.

        Args:
            audio_data: Binary audio data

        Returns:
            str: Transcribed text

        Raises:
            ValueError: If the audio file is empty or invalid
            RuntimeError: If the transcription fails
        """
        if not audio_data:
            raise ValueError("Audio data cannot be empty")

        try:
            # Chainlit sends raw PCM — wrap in a proper WAV container
            wav_buffer = BytesIO()
            with wave.open(wav_buffer, "wb") as wav_file:
                wav_file.setnchannels(1)       # mono
                wav_file.setsampwidth(2)       # 16-bit
                wav_file.setframerate(24000)   # matches Chainlit config sample_rate
                wav_file.writeframes(audio_data)

            wav_buffer.seek(0)
            wav_buffer.name = "audio.wav"


            transcription = self.client.audio.transcriptions.create(
                file=wav_buffer,
                model="whisper-large-v3-turbo",
                language="en",
                response_format="text",
            )

            if not transcription:
                raise SpeechToTextError("Transcription result is empty")
            return transcription
        except Exception as e:
            raise SpeechToTextError(f"Speech-to-text conversion failed: {str(e)}") from e