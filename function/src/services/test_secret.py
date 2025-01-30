# from utils.logger import logger
# from utils.constants import USERNAME, TARGETS
# from repository import secrets_manager, ssh, ssm

# def execute(secret_id: str, client_token: str) -> None:
#    try:
#        logger.info({
#            "msg": "Starting secret testing",
#            "secret_id": secret_id
#        })

#        pending_dict = secrets_manager.get_secret_dict(secret_id, "AWSPENDING")
       
#        try:
#            logger.info({
#                "msg": "Retrieving target instances", 
#                "secret_id": secret_id
#            })
#            ip_addresses = ssm.get_addrs_for_add_key(client_token)
           
#            logger.info({
#                "msg": "Testing SSH connection",
#                "ip_count": len(ip_addresses),
#                "target_ips": ip_addresses,
#                "username": USERNAME,
#                "secret_id": secret_id
#            })

#            if not ip_addresses:
#                raise ValueError("No target instances found")

#            ssh.run_command(
#                ip_addresses=ip_addresses,
#                username=USERNAME,
#                private_key=pending_dict['PrivateKey'],
#                command='hostname'
#            )

#            logger.info({
#                "msg": "Successfully tested SSH connections",
#                "tested_ips": ip_addresses,
#                "username": USERNAME,
#                "secret_id": secret_id,
               
#            })
           
#        except ValueError as e:
#            logger.error({
#                "msg": "No target instances found",
#                "targets": TARGETS,
#                "error": str(e)
#            })
#            raise
           
#    except Exception as e:
#        logger.error({
#            "msg": "Failed testing secret",
#            "secret_id": secret_id,
#            "error": str(e)
#        })
#        raise
from utils.logger import logger
from repository import secrets_manager, ssh, ssm

def execute(secret_id: str, client_token: str) -> None:
    try:
        logger.info({
            "msg": "Starting secret testing",
            "secret_id": secret_id
        })

        pending_dict = secrets_manager.get_secret_dict(secret_id, "AWSPENDING")
        username = secrets_manager.get_username(pending_dict)
        
        try:
            logger.info({
                "msg": "Retrieving target instances", 
                "secret_id": secret_id
            })
            ip_addresses = ssm.get_addrs_for_add_key(secret_id, client_token)
            
            logger.info({
                "msg": "Testing SSH connection",
                "ip_count": len(ip_addresses),
                "target_ips": ip_addresses,
                "username": username,
                "secret_id": secret_id
            })

            if not ip_addresses:
                raise ValueError("No target instances found")

            ssh.run_command(
                ip_addresses=ip_addresses,
                username=username,
                private_key=pending_dict['PrivateKey'],
                command='hostname'
            )

            logger.info({
                "msg": "Successfully tested SSH connections",
                "tested_ips": ip_addresses,
                "username": username,
                "secret_id": secret_id
            })
            
        except ValueError as e:
            logger.error({
                "msg": "No target instances found",
                "error": str(e)
            })
            raise
            
    except Exception as e:
        logger.error({
            "msg": "Failed testing secret",
            "secret_id": secret_id,
            "error": str(e)
        })
        raise