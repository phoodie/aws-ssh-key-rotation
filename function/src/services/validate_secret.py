# from typing import Dict, Any
# from utils.logger import logger
# from utils.constants import USERNAME, TARGETS
# from repository import secrets_manager

# def validate_rotation(secret_id: str, token: str) -> Dict[str, Any]:
#     try:
#         # Validate environment first
#         if not all([USERNAME, TARGETS]):
#             raise ValueError("Missing required environment configuration")

#         # Get secret metadata from repository
#         metadata = secrets_manager.get_secret_metadata(secret_id)
        
#         # Check if rotation is enabled
#         if not metadata['RotationEnabled']:
#             raise ValueError(f"Secret {secret_id} is not enabled for rotation")

#         # Get version stages
#         versions = metadata['VersionIdsToStages']
        
#         # Validate version exists
#         if token not in versions:
#             raise ValueError(f"Secret version {token} has no stage for rotation")

#         # Check if already current
#         if "AWSCURRENT" in versions[token]:
#             logger.info({
#                 "msg": "Secret version already marked as AWSCURRENT",
#                 "secret_id": secret_id,
#                 "token": token
#             })
#             return {
#                 "should_proceed": False,
#                 "message": "Secret version already current"
#             }

#         # Check for pending state
#         if "AWSPENDING" not in versions[token]:
#             raise ValueError(f"Secret version {token} not set as AWSPENDING")
        
#         return {
#             "should_proceed": True,
#             "message": "Validation successful"
#         }
        
#     except Exception as e:
#         logger.error({
#             "msg": "Secret validation failed",
#             "secret_id": secret_id,
#             "error": str(e)
#         })
#         raise
from typing import Dict, Any
from utils.logger import logger
from repository import secrets_manager

def validate_secret_structure(secret_dict: Dict[str, Any]) -> None:
    """Validate the structure of the secret value."""
    if 'username' not in secret_dict:
        raise ValueError("Missing required field 'username' in secret")
        
    if 'ec2-arn' not in secret_dict:
        raise ValueError("Missing required field 'ec2-arn' in secret")
        
    instance_arns = secret_dict.get('ec2-arn')
    if not isinstance(instance_arns, (list, str)):
        raise ValueError("Field 'ec2-arn' must be a string or list of strings")
        
    if isinstance(instance_arns, list) and not all(isinstance(arn, str) for arn in instance_arns):
        raise ValueError("All EC2 ARNs must be strings")

def validate_rotation(secret_id: str, token: str) -> Dict[str, Any]:
    """
    Validates the business logic for secret rotation.
    """
    try:
        # Get secret metadata and validate structure
        metadata = secrets_manager.get_secret_metadata(secret_id)
        current_secret = secrets_manager.get_secret_dict(
            secret_id=secret_id,
            stage="AWSCURRENT"
        )
        
        # Extract and log key information
        username = secrets_manager.get_username(current_secret)
        instance_arns = secrets_manager.get_instance_arns(current_secret)
        
        logger.info({
            "msg": "Retrieved secret configuration",
            "secret_id": secret_id,
            "username": username,
            "instance_count": len(instance_arns),
            "instance_arns": instance_arns
        })
        
        # Validate secret structure
        validate_secret_structure(current_secret)
        
        # Check if rotation is enabled
        if not metadata['RotationEnabled']:
            raise ValueError(f"Secret {secret_id} is not enabled for rotation")

        # Get version stages
        versions = metadata['VersionIdsToStages']
        
        # Validate version exists
        if token not in versions:
            raise ValueError(f"Secret version {token} has no stage for rotation")

        # Check if already current
        if "AWSCURRENT" in versions[token]:
            logger.info({
                "msg": "Secret version already marked as AWSCURRENT",
                "secret_id": secret_id,
                "token": token
            })
            return {
                "should_proceed": False,
                "message": "Secret version already current"
            }

        # Check for pending state
        if "AWSPENDING" not in versions[token]:
            raise ValueError(f"Secret version {token} not set as AWSPENDING")
        
        return {
            "should_proceed": True,
            "message": "Validation successful"
        }
        
    except Exception as e:
        logger.error({
            "msg": "Secret validation failed",
            "secret_id": secret_id,
            "error": str(e)
        })
        raise