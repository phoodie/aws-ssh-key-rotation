from typing import Dict, Any, Optional
from utils.logger import logger

def validate_rotation_event(event: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # Handle both direct Lambda invocation and EventBridge events
        detail = event.get('detail', event)
        
        # Required fields for rotation
        required_fields = ['Step', 'SecretId', 'ClientRequestToken']
        
        # Validate required fields
        missing_fields = [
            field for field in required_fields 
            if not detail.get(field)
        ]
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
            
        # Validate step value
        valid_steps = {'createSecret', 'setSecret', 'testSecret', 'finishSecret'}
        if detail['Step'] not in valid_steps:
            raise ValueError(f"Invalid rotation step: {detail['Step']}")
            
        # Return validated detail
        return {
            'step': detail['Step'],
            'secret_id': detail['SecretId'],
            'token': detail['ClientRequestToken']
        }
        
    except Exception as e:
        logger.error({
            "msg": "Event validation failed",
            "event": event,
            "error": str(e)
        })
        raise