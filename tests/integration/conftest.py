from pathlib import Path

import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient

# Load real .env BEFORE any app module is imported.
# override=True ensures these replace the fake values set by the parent conftest.
load_dotenv(override=True)

from interfaces.whatsapp.webhook_endpoint import app

ASSETS_DIR = Path(__file__).parent.parent.parent / "assets"


@pytest.fixture(scope="session")
def audio_bytes():
    return (ASSETS_DIR / "recording_asking_time.mp3").read_bytes()


@pytest.fixture(scope="session")
def image_bytes():
    return (ASSETS_DIR / "download.jpeg").read_bytes()


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
