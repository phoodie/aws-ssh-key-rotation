# from typing import Dict, Any
# from utils.logger import logger
# from utils.event_validator import validate_rotation_event
# from services import validate_secret as validate_secret_service

# def handle_event(event: Dict[str, Any]) -> Dict[str, Any]:
#     try:
#         # Validate event structure
#         validated_event = validate_rotation_event(event)
        
#         # Call service layer for business logic validation
#         validation_result = validate_secret_service.validate_rotation(
#             secret_id=validated_event['secret_id'],
#             token=validated_event['token']
#         )
        
#         if not validation_result['should_proceed']:
#             return {
#                 "statusCode": 200,
#                 "body": validation_result['message']
#             }

#         return {
#             "statusCode": 200,
#             "detail": validated_event
#         }

#     except Exception as e:
#         logger.error({
#             "msg": "Event validation failed",
#             "error": str(e)
#         })
#         raise
from typing import Dict, Any, Optional
from utils.logger import logger
from utils.event_validator import validate_rotation_event
from services import validate_secret as validate_secret_service

def validate_and_process_event(event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Validates and processes the rotation event.
    Returns validated event details if successful, None if validation fails.
    """
    try:
        # Validate event structure
        validated_event = validate_rotation_event(event)
        
        # Call service layer for business logic validation
        validation_result = validate_secret_service.validate_rotation(
            secret_id=validated_event['secret_id'],
            token=validated_event['token']
        )
        
        if not validation_result['should_proceed']:
            logger.info({
                "msg": "Validation indicated no further action needed",
                "reason": validation_result['message']
            })
            return None
            
        return validated_event
        
    except Exception as e:
        logger.error({
            "msg": "Event validation failed",
            "error": str(e)
        })
        raise

def handle_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Legacy event handler for backward compatibility.
    """
    try:
        # Validate event structure
        validated_event = validate_rotation_event(event)
        
        # Call service layer for business logic validation
        validation_result = validate_secret_service.validate_rotation(
            secret_id=validated_event['secret_id'],
            token=validated_event['token']
        )
        
        if not validation_result['should_proceed']:
            return {
                "statusCode": 200,
                "body": validation_result['message']
            }

        return {
            "statusCode": 200,
            "detail": validated_event
        }

    except Exception as e:
        logger.error({
            "msg": "Event validation failed",
            "error": str(e)
        })
        raise