from typing import Any
from utils.logger import logger
from services import set_secret as set_secret_service

def handle(secret_id: str, client_token: str) -> None:
    logger.info({
        "msg": "Deploying public key",
        "secret_id": secret_id
    })
    set_secret_service.execute(secret_id, client_token)