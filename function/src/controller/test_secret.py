from typing import Any
from utils.logger import logger
from services import test_secret as test_secret_service

def handle(secret_id: str, client_token: str) -> None:
    logger.info({
        "msg": "Testing SSH connection",
        "secret_id": secret_id
    })
    test_secret_service.execute(secret_id, client_token)