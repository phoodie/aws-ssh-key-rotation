# from utils.logger import logger
# from utils.constants import USERNAME
# from repository import secrets_manager, ssm

# def execute(secret_id: str, client_token: str) -> None:
#     try:
#         logger.info({
#             "msg": "Finishing secret rotation",
#             "secret_id": secret_id
#         })

#         current_version = secrets_manager.get_current_version(secret_id)
        
#         if current_version == client_token:
#             logger.info({
#                 "msg": "Version already current",
#                 "secret_id": secret_id
#             })
#             return
            
#         secrets_manager.update_secret_stage(
#             secret_id=secret_id,
#             move_to_version=client_token,
#             remove_from_version=current_version,
#             stage="AWSCURRENT"
#         )
        
#         if current_version:
#             command_id = ssm.del_public_key(USERNAME, current_version)
#             logger.info({
#                 "msg": "Successfully finished secret rotation",
#                 "secret_id": secret_id,
#                 "command_id": command_id
#             })
            
#     except Exception as e:
#         logger.error({
#             "msg": "Failed finishing secret rotation",
#             "secret_id": secret_id,
#             "error": str(e)
#         })
#         raise
from utils.logger import logger
from repository import secrets_manager, ssm

def execute(secret_id: str, client_token: str) -> None:
    """
    Finish the secret rotation by updating the version stages and cleaning up old keys.
    """
    try:
        logger.info({
            "msg": "Finishing secret rotation",
            "secret_id": secret_id
        })

        current_version = secrets_manager.get_current_version(secret_id)
        
        if current_version == client_token:
            logger.info({
                "msg": "Version already current",
                "secret_id": secret_id
            })
            return
            
        # Get current secret to get username
        current_secret = secrets_manager.get_secret_dict(
            secret_id=secret_id,
            stage="AWSCURRENT"
        )
        username = secrets_manager.get_username(current_secret)
            
        # Update the version stages
        secrets_manager.update_secret_stage(
            secret_id=secret_id,
            move_to_version=client_token,
            remove_from_version=current_version,
            stage="AWSCURRENT"
        )
        
        # Remove the old public key if there was a previous version
        if current_version:
            command_id = ssm.del_public_key(
                secret_id=secret_id,
                username=username,
                previous_version=current_version
            )
            logger.info({
                "msg": "Successfully finished secret rotation",
                "secret_id": secret_id,
                "username": username,
                "command_id": command_id
            })
            
    except Exception as e:
        logger.error({
            "msg": "Failed finishing secret rotation",
            "secret_id": secret_id,
            "error": str(e)
        })
        raise