from typing import Dict, Any
from utils.logger import logger
from utils.constants import MODULE_VERSION, SNSARN, SSMROLE
from controller import validate_secret, create_secret, set_secret, test_secret, finish_secret

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        logger.info({
            "msg": "Starting aws-ssh-key-rotation lambda function",
            "sns_arn": SNSARN,
            "ServiceRoleARN": SSMROLE,
            "module_version": MODULE_VERSION
        })

        # Validate event through controller layer
        event_details = validate_secret.validate_and_process_event(event)
        if not event_details:
            return {
                "statusCode": 400,
                "body": "validate secret failed"
            }

        # Extract validated event details
        step = event_details['step']
        secret_id = event_details['secret_id']
        token = event_details['token']

        # Update logger step based on validated event
        logger.step = step

        # Execute the appropriate step handler
        if step == "createSecret":
            create_secret.handle(
                secret_id=secret_id,
                client_token=token
            )
        elif step == "setSecret":
            set_secret.handle(
                secret_id=secret_id,
                client_token=token
            )
        elif step == "testSecret":
            test_secret.handle(
                secret_id=secret_id,
                client_token=token
            )
        elif step == "finishSecret":
            finish_secret.handle(
                secret_id=secret_id,
                client_token=token
            )
        else:
            raise ValueError(f"Invalid rotation step: {step}")

        logger.info({
            "msg": f"Successfully completed {step} rotation step",
            "secret_id": secret_id
        })

        return {
            "statusCode": 200,
            "body": f"Successfully completed {step} step"
        }

    except Exception as e:
        step = getattr(logger, 'step', 'Unknown')
        logger.error({
            "msg": f"Failed {step} rotation step",
            "error": str(e)
        })
        raise