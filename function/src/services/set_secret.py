# from utils.logger import logger
# from utils.constants import USERNAME
# from repository import secrets_manager, ssm

# def execute(secret_id: str, client_token: str) -> None:
#     try:
#         logger.info({
#             "msg": "Adding public key via SSM",
#             "secret_id": secret_id
#         })
        
#         pending_dict = secrets_manager.get_secret_dict(
#             secret_id=secret_id,
#             stage="AWSPENDING"
#         )
        
#         command_id = ssm.add_public_key(
#             username=USERNAME,
#             public_key=pending_dict['PublicKey'],
#             new_version=client_token
#         )
        
#         logger.info({
#             "msg": "Successfully added public key",
#             "secret_id": secret_id,
#             "command_id": command_id
#         })

#     except Exception as e:
#         logger.error({
#             "msg": "Failed to add public key",
#             "secret_id": secret_id,
#             "error": str(e)
#         })
#         raise
from utils.logger import logger
from repository import secrets_manager, ssm

def execute(secret_id: str, client_token: str) -> None:
    try:
        logger.info({
            "msg": "Adding public key via SSM",
            "secret_id": secret_id
        })
        
        pending_dict = secrets_manager.get_secret_dict(
            secret_id=secret_id,
            stage="AWSPENDING"
        )
        
        # Get username from the secret
        username = secrets_manager.get_username(pending_dict)
        
        command_id = ssm.add_public_key(
            secret_id=secret_id,
            username=username,
            public_key=pending_dict['PublicKey'],
            new_version=client_token
        )
        
        logger.info({
            "msg": "Successfully added public key",
            "secret_id": secret_id,
            "username": username,
            "command_id": command_id
        })

    except Exception as e:
        logger.error({
            "msg": "Failed to add public key",
            "secret_id": secret_id,
            "error": str(e)
        })
        raise