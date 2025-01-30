# from utils.logger import logger
# from repository import ssh, secrets_manager

# def execute(secret_id: str, client_token: str) -> None:
#     try:
#         logger.info({
#             "msg": "Creating new secret version",
#             "secret_id": secret_id
#         })
        
#         try:
#             secrets_manager.get_secret_dict(
#                 secret_id=secret_id,
#                 stage="AWSPENDING",
#                 token=client_token
#             )
#             logger.info({
#                 "msg": "AWSPENDING version exists, skipping creation",
#                 "secret_id": secret_id
#             })
#             return
#         except secrets_manager.get_client().exceptions.ResourceNotFoundException:
#             pass

#         private_key, public_key = ssh.generate_key_pair(client_token)
        
#         secrets_manager.store_key_pair(
#             secret_id=secret_id,
#             client_token=client_token,
#             private_key=private_key,
#             public_key=public_key
#         )
        
#         logger.info({
#             "msg": "Successfully created new secret version",
#             "secret_id": secret_id
#         })
        
#     except Exception as e:
#         logger.error({
#             "msg": "Failed creating secret",
#             "secret_id": secret_id,
#             "error": str(e)
#         })
#         raise

from utils.logger import logger
from repository import ssh, secrets_manager

def execute(secret_id: str, client_token: str) -> None:
    try:
        logger.info({
            "msg": "Starting secret creation",
            "secret_id": secret_id
        })
        
        # Check if AWSPENDING version exists
        try:
            pending_secret = secrets_manager.get_secret_dict(
                secret_id=secret_id,
                stage="AWSPENDING",
                token=client_token
            )
            logger.info({
                "msg": "AWSPENDING version exists, skipping creation",
                "secret_id": secret_id
            })
            return
        except secrets_manager.get_client().exceptions.ResourceNotFoundException:
            pass

        # Get current secret to preserve username and instance ARNs
        current_secret = secrets_manager.get_secret_dict(
            secret_id=secret_id,
            stage="AWSCURRENT"
        )
        
        username = secrets_manager.get_username(current_secret)
        instance_arns = secrets_manager.get_instance_arns(current_secret)

        logger.info({
            "msg": "Retrieved current secret configuration",
            "secret_id": secret_id,
            "username": username,
            "instance_count": len(instance_arns),
            "instance_arns": instance_arns
        })

        # Generate new SSH key pair
        private_key, public_key = ssh.generate_key_pair(client_token)
        
        # Store new version with existing username and instance ARNs
        secrets_manager.store_secret_values(
            secret_id=secret_id,
            client_token=client_token,
            username=username,
            instance_arns=instance_arns,
            private_key=private_key,
            public_key=public_key
        )
        
        logger.info({
            "msg": "Successfully created new secret version",
            "secret_id": secret_id,
            "username": username,
            "instance_count": len(instance_arns),
            "instance_arns": instance_arns
        })
        
    except Exception as e:
        logger.error({
            "msg": "Failed creating secret",
            "secret_id": secret_id,
            "error": str(e)
        })
        raise