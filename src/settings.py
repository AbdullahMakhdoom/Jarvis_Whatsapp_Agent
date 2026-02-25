from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")

    OPENAI_API_KEY: str
    TEXT_MODEL_NAME: str = "gpt-5-nano-2025-08-07"
    SMALL_TEXT_MODEL_NAME: str = "gpt-5-nano-2025-08-07"

    GROQ_API_KEY: str
    ELEVENLABS_API_KEY: str
    ELEVENLABS_VOICE_ID: str
    STT_MODEL_NAME: str = "whisper-large-v3-turbo"
    TTS_MODEL_NAME: str = "eleven_flash_v2_5"

    TOTAL_MESSAGES_SUMMARY_TRIGGER: int = 10
    TOTAL_MESSAGES_AFTER_SUMMARY: int = 3

    SHORT_TERM_MEMORY_DB_PATH: str = "/app/data/memory.db"

    QDRANT_API_KEY: str | None
    QDRANT_URL: str
    QDRANT_PORT: str = "6333"
    QDRANT_HOST: str | None = None

    MEMORY_TOP_K: int = 3
    ROUTER_MESSAGES_TO_ANALYZE: int = 3

settings = Settings()