import logging

from fastapi import FastAPI

from .whatsapp_response import whatsapp_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

app = FastAPI()
app.include_router(whatsapp_router)