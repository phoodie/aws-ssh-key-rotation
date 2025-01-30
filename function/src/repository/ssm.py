# import boto3
# import datetime
# from typing import List, Dict, Any
# from utils.constants import TARGETS, SNSARN, SSMROLE
# from repository import ec2

# def get_client():
#    return boto3.client('ssm')

# def send_command(targets: List[dict], commands: List[str], action: str, version: str) -> Dict[str, Any]:
#    return get_client().send_command(
#        Targets=targets,
#        DocumentName="AWS-RunShellScript",
#        Comment=f"{action} {version}",
#        Parameters={'commands': commands},
#        ServiceRoleArn=SSMROLE,
#        NotificationConfig={
#            'NotificationArn': SNSARN,
#            'NotificationEvents': ['Failed', 'TimedOut'], #only need failed and timeout, this is testing SNS
#            'NotificationType': 'Command'
#         }
#    )
   
# def add_public_key(username: str, public_key: str, new_version: str) -> str:
#    commands = f"""
# key_file=~{username}/.ssh/authorized_keys
# COUNT=`grep -c "{new_version}" $key_file`
# if [ $COUNT -eq 0 ]
# then
#    echo "Adding public key with comment {new_version} to authorized_keys file for {username}"
#    echo "{public_key}" >> $key_file
# else
#    echo "Public key with comment {new_version} already exists"
# fi
# """.strip().split('\n')
  
#    response = send_command(
#        targets=TARGETS,
#        commands=commands,
#        action='add_key',
#        version=new_version
#    )
#    return response['Command']['CommandId']

# def del_public_key(username: str, previous_version: str) -> str:
#    commands = f"""
# key_file=~{username}/.ssh/authorized_keys
# echo "Removing public key with comment {previous_version} from authorized_keys file for {username}"
# sed -i".bak" "/{previous_version}/d" $key_file
# """.strip().split('\n')
  
#    response = send_command(
#        targets=TARGETS,
#        commands=commands,
#        action='delete_key',
#        version=previous_version
#    )
#    return response['Command']['CommandId']

# def get_addrs_for_add_key(new_version: str) -> List[str]:
#    ssm = get_client()
#    instance_ids = []
#    paginator = ssm.get_paginator('list_commands')

#    now = datetime.datetime.now()
#    search_start = now - datetime.timedelta(hours=4) 
#    search_start_iso = search_start.replace(microsecond=0).isoformat() + 'Z'
#    search_comment = f"add_key {new_version}"
#    command_id = None
   
#    for page in paginator.paginate(Filters=[{
#            'key': 'InvokedAfter',
#            'value': search_start_iso
#        }]):
#        for cmd in page['Commands']:
#            if 'Comment' in cmd and cmd['Comment'] == search_comment and cmd['Status'] == 'Success':
#                command_id = cmd['CommandId']
#                break

#    if command_id is None:
#        raise ValueError(f"Could not find successful Run Command with comment 'add_key {new_version}'")

#    paginator = ssm.get_paginator('list_command_invocations')
#    for page in paginator.paginate(CommandId=command_id):
#        for cmd in page['CommandInvocations']:
#            instance_ids.append(cmd['InstanceId'])

#    return ec2.get_instance_private_ips(instance_ids)
import boto3
import datetime
from typing import List, Dict, Any
from utils.constants import SNSARN, SSMROLE
from repository import ec2, secrets_manager

def get_client():
    return boto3.client('ssm')

def get_instance_ids_from_arns(instance_arns: List[str]) -> List[str]:
    """Extract instance IDs from ARNs."""
    return [arn.split('/')[-1] for arn in instance_arns]

def send_command(instance_ids: List[str], commands: List[str], action: str, version: str) -> Dict[str, Any]:
    """Send SSM command to specific instance IDs."""
    return get_client().send_command(
        InstanceIds=instance_ids,
        DocumentName="AWS-RunShellScript",
        Comment=f"{action} {version}",
        Parameters={'commands': commands},
        ServiceRoleArn=SSMROLE,
        NotificationConfig={
            'NotificationArn': SNSARN,
            'NotificationEvents': ['Failed', 'TimedOut'],
            'NotificationType': 'Command'
        }
    )

def add_public_key(secret_id: str, username: str, public_key: str, new_version: str) -> str:
    """Add public key to authorized_keys file on target instances."""
    # Get instance ARNs from secret
    secret_dict = secrets_manager.get_secret_dict(secret_id, "AWSCURRENT")
    instance_arns = secrets_manager.get_instance_arns(secret_dict)
    instance_ids = get_instance_ids_from_arns(instance_arns)

    commands = f"""
key_file=~{username}/.ssh/authorized_keys
COUNT=`grep -c "{new_version}" $key_file`
if [ $COUNT -eq 0 ]
then
    echo "Adding public key with comment {new_version} to authorized_keys file for {username}"
    echo "{public_key}" >> $key_file
else
    echo "Public key with comment {new_version} already exists"
fi
""".strip().split('\n')

    response = send_command(
        instance_ids=instance_ids,
        commands=commands,
        action='add_key',
        version=new_version
    )
    return response['Command']['CommandId']

def del_public_key(secret_id: str, username: str, previous_version: str) -> str:
    """Remove public key from authorized_keys file on target instances."""
    # Get instance ARNs from secret
    secret_dict = secrets_manager.get_secret_dict(secret_id, "AWSCURRENT")
    instance_arns = secrets_manager.get_instance_arns(secret_dict)
    instance_ids = get_instance_ids_from_arns(instance_arns)

    commands = f"""
key_file=~{username}/.ssh/authorized_keys
echo "Removing public key with comment {previous_version} from authorized_keys file for {username}"
sed -i".bak" "/{previous_version}/d" $key_file
""".strip().split('\n')

    response = send_command(
        instance_ids=instance_ids,
        commands=commands,
        action='delete_key',
        version=previous_version
    )
    return response['Command']['CommandId']

def get_addrs_for_add_key(secret_id: str, new_version: str) -> List[str]:
    """Get private IPs of instances where the key was successfully added."""
    ssm = get_client()
    instance_ids = []
    paginator = ssm.get_paginator('list_commands')

    now = datetime.datetime.now()
    search_start = now - datetime.timedelta(hours=4)
    search_start_iso = search_start.replace(microsecond=0).isoformat() + 'Z'
    search_comment = f"add_key {new_version}"
    command_id = None
    
    for page in paginator.paginate(Filters=[{
            'key': 'InvokedAfter',
            'value': search_start_iso
        }]):
        for cmd in page['Commands']:
            if 'Comment' in cmd and cmd['Comment'] == search_comment and cmd['Status'] == 'Success':
                command_id = cmd['CommandId']
                break

    if command_id is None:
        raise ValueError(f"Could not find successful Run Command with comment 'add_key {new_version}'")

    paginator = ssm.get_paginator('list_command_invocations')
    for page in paginator.paginate(CommandId=command_id):
        for cmd in page['CommandInvocations']:
            instance_ids.append(cmd['InstanceId'])

    return ec2.get_instance_private_ips(instance_ids)