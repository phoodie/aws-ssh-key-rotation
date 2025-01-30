from typing import Any
from utils.logger import logger
from services import finish_secret as finish_secret_service

def handle(secret_id: str, client_token: str) -> None:
    logger.info({
        "msg": "Completing rotation",
        "secret_id": secret_id
    })
    finish_secret_service.execute(secret_id, client_token)