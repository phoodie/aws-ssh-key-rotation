from typing import Any
from utils.logger import logger
from services import create_secret as create_secret_service

def handle(secret_id: str, client_token: str) -> None:
    logger.info({
        "msg": "Creating new secret version",
        "secret_id": secret_id
    })
    create_secret_service.execute(secret_id, client_token)