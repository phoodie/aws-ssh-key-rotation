# import boto3
# import json
# from typing import Dict, Any, Optional

# def get_client():
#    return boto3.client('secretsmanager')

# def get_secret_dict(secret_id: str, stage: str, token: Optional[str] = None) -> Dict[str, Any]:
#    client = get_client()
#    kwargs = {
#        'SecretId': secret_id,
#        'VersionStage': stage
#    }
#    if token:
#        kwargs['VersionId'] = token
       
#    secret = client.get_secret_value(**kwargs)
#    return json.loads(secret['SecretString'])

# def store_key_pair(
#    secret_id: str,
#    client_token: str,
#    private_key: str,
#    public_key: str
# ) -> None:
#    client = get_client()
#    secret_dict = {
#        'PrivateKey': private_key,
#        'PublicKey': public_key
#    }
   
#    client.put_secret_value(
#        SecretId=secret_id,
#        ClientRequestToken=client_token,
#        SecretString=json.dumps(secret_dict),
#        VersionStages=['AWSPENDING']
#    )

# def get_secret_metadata(secret_id: str) -> Dict[str, Any]:
#    client = get_client()
#    return client.describe_secret(SecretId=secret_id)

# def get_current_version(secret_id: str) -> Optional[str]:
#    metadata = get_secret_metadata(secret_id)
#    for version in metadata["VersionIdsToStages"]:
#        if "AWSCURRENT" in metadata["VersionIdsToStages"][version]:
#            return version
#    return None

# def update_secret_stage(
#    secret_id: str, 
#    move_to_version: str,
#    remove_from_version: str,
#    stage: str = "AWSCURRENT"
# ) -> None:
#    client = get_client()
#    client.update_secret_version_stage(
#        SecretId=secret_id,
#        VersionStage=stage,
#        MoveToVersionId=move_to_version,
#        RemoveFromVersionId=remove_from_version
#    )

# ## NEW WOEKING STATE
# import boto3
# import json
# from typing import Dict, Any, Optional, List

# def get_client():
#     return boto3.client('secretsmanager')

# def get_secret_metadata(secret_id: str) -> Dict[str, Any]:
#     """Get metadata about the secret."""
#     client = get_client()
#     return client.describe_secret(SecretId=secret_id)

# def get_secret_dict(secret_id: str, stage: str, token: Optional[str] = None) -> Dict[str, Any]:
#     """Get the secret value as a dictionary."""
#     client = get_client()
#     kwargs = {
#         'SecretId': secret_id,
#         'VersionStage': stage
#     }
#     if token:
#         kwargs['VersionId'] = token
        
#     secret = client.get_secret_value(**kwargs)
#     return json.loads(secret['SecretString'])

# def get_instance_arns(secret_dict: Dict[str, Any]) -> List[str]:
#     """Extract EC2 instance ARNs from secret value."""
#     instance_arns = secret_dict.get('ec2-arn', [])
#     if isinstance(instance_arns, str):
#         instance_arns = [instance_arns]  # Convert single ARN to list
#     return instance_arns

# def get_username(secret_dict: Dict[str, Any]) -> str:
#     """Extract username from secret value."""
#     username = secret_dict.get('username')
#     if not username:
#         raise ValueError("Username not found in secret")
#     return username

# def get_current_version(secret_id: str) -> Optional[str]:
#     """Get the current version ID of the secret."""
#     metadata = get_secret_metadata(secret_id)
#     for version in metadata["VersionIdsToStages"]:
#         if "AWSCURRENT" in metadata["VersionIdsToStages"][version]:
#             return version
#     return None

# def store_secret_values(
#     secret_id: str,
#     client_token: str,
#     username: str,
#     instance_arns: List[str],
#     private_key: str,
#     public_key: str
# ) -> None:
#     """Store all secret values including SSH keys."""
#     client = get_client()
#     secret_dict = {
#         'username': username,
#         'ec2-arn': instance_arns,
#         'PrivateKey': private_key,
#         'PublicKey': public_key
#     }
    
#     client.put_secret_value(
#         SecretId=secret_id,
#         ClientRequestToken=client_token,
#         SecretString=json.dumps(secret_dict),
#         VersionStages=['AWSPENDING']
#     )

# def update_secret_stage(
#     secret_id: str, 
#     move_to_version: str,
#     remove_from_version: str,
#     stage: str = "AWSCURRENT"
# ) -> None:
#     """Update the version stages of the secret."""
#     client = get_client()
#     client.update_secret_version_stage(
#         SecretId=secret_id,
#         VersionStage=stage,
#         MoveToVersionId=move_to_version,
#         RemoveFromVersionId=remove_from_version
#     )
import boto3
import json
from typing import Dict, Any, Optional, List

def get_client():
    return boto3.client('secretsmanager')

def get_secret_metadata(secret_id: str) -> Dict[str, Any]:
    """Get metadata about the secret."""
    client = get_client()
    return client.describe_secret(SecretId=secret_id)

def get_current_version(secret_id: str) -> Optional[str]:
    """Get the current version ID of the secret."""
    metadata = get_secret_metadata(secret_id)
    for version in metadata["VersionIdsToStages"]:
        if "AWSCURRENT" in metadata["VersionIdsToStages"][version]:
            return version
    return None

def store_secret_values(
    secret_id: str,
    client_token: str,
    username: str,
    instance_arns: List[str],
    private_key: str,
    public_key: str
) -> None:
    """
    Store secret values in a format compatible with Secrets Manager key-value view.
    Each value must be a string for key-value pair compatibility.
    """
    client = get_client()
    secret_dict = {
        'username': username,
        'ec2-arn': json.dumps(instance_arns),  # Convert list to JSON string
        'private-key': private_key,            # Changed from PrivateKey
        'public-key': public_key               # Changed from PublicKey
    }
    
    client.put_secret_value(
        SecretId=secret_id,
        ClientRequestToken=client_token,
        SecretString=json.dumps(secret_dict),
        VersionStages=['AWSPENDING']
    )

def get_instance_arns(secret_dict: Dict[str, Any]) -> List[str]:
    """Extract EC2 instance ARNs from secret value."""
    instance_arns = secret_dict.get('ec2-arn')
    if isinstance(instance_arns, str):
        try:
            # Parse the JSON string back into a list
            instance_arns = json.loads(instance_arns)
        except json.JSONDecodeError:
            # If it's a single ARN string, wrap it in a list
            instance_arns = [instance_arns]
    return instance_arns if isinstance(instance_arns, list) else []

def get_secret_dict(secret_id: str, stage: str, token: Optional[str] = None) -> Dict[str, Any]:
    """Get and parse the secret value."""
    client = get_client()
    kwargs = {
        'SecretId': secret_id,
        'VersionStage': stage
    }
    if token:
        kwargs['VersionId'] = token
        
    secret = client.get_secret_value(**kwargs)
    secret_dict = json.loads(secret['SecretString'])
    
    # Convert stored private/public key names back to original format if needed
    if 'private-key' in secret_dict:
        secret_dict['PrivateKey'] = secret_dict.pop('private-key')
    if 'public-key' in secret_dict:
        secret_dict['PublicKey'] = secret_dict.pop('public-key')
        
    return secret_dict

def get_username(secret_dict: Dict[str, Any]) -> str:
    """Extract username from secret value."""
    username = secret_dict.get('username')
    if not username:
        raise ValueError("Username not found in secret")
    return username

def update_secret_stage(
    secret_id: str, 
    move_to_version: str,
    remove_from_version: str,
    stage: str = "AWSCURRENT"
) -> None:
    """Update the version stages of the secret."""
    client = get_client()
    client.update_secret_version_stage(
        SecretId=secret_id,
        VersionStage=stage,
        MoveToVersionId=move_to_version,
        RemoveFromVersionId=remove_from_version
    )