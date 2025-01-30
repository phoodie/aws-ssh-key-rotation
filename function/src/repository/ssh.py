from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import paramiko
import io
from typing import List, Tuple

def generate_key_pair(comment: str) -> Tuple[str, str]:
   key = rsa.generate_private_key(
       backend=default_backend(),
       public_exponent=65537,
       key_size=2048
   )
  
   private_key = key.private_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PrivateFormat.TraditionalOpenSSL,
       encryption_algorithm=serialization.NoEncryption()
   )
  
   public_key = key.public_key().public_bytes(
       serialization.Encoding.OpenSSH,
       serialization.PublicFormat.OpenSSH
   )
  
   return (
       private_key.decode('utf-8'),
       f"{public_key.decode('utf-8')} {comment}"
   )

def run_command(ip_addresses: List[str], username: str, private_key: str, command: str) -> None:
   private_key_str = io.StringIO()
   private_key_str.write(private_key)
   private_key_str.seek(0)
   key = paramiko.RSAKey.from_private_key(private_key_str)
  
   client = paramiko.client.SSHClient()
   client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  
   for ip in ip_addresses:
       try:
           client.connect(
               hostname=ip,
               username=username,
               pkey=key,
               look_for_keys=False
           )
           
           client.exec_command(command)
           
       finally:
           client.close()