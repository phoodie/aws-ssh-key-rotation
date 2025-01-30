from typing import List, Dict, Any
import boto3

def get_client():
   return boto3.client('ec2')

def get_instance_private_ips(instance_ids: List[str]) -> List[str]:
   if not instance_ids:
       return []
       
   ec2 = get_client()
   paginator = ec2.get_paginator('describe_instances')
   private_ips = []
  
   filters = [{
       "Name": "instance-id",
       "Values": instance_ids
   }]

   for page in paginator.paginate(Filters=filters):
       for reservation in page['Reservations']:
           for instance in reservation['Instances']:
               if instance['NetworkInterfaces']:
                   primary_interface = instance['NetworkInterfaces'][0]
                   private_ip = primary_interface['PrivateIpAddress']
                   private_ips.append(private_ip)

   return private_ips

def get_instance_metadata(instance_ids: List[str]) -> List[Dict[str, Any]]:
   if not instance_ids:
       return []
       
   ec2 = get_client()
   paginator = ec2.get_paginator('describe_instances')
   instances = []
  
   filters = [{
       "Name": "instance-id",
       "Values": instance_ids
   }]

   for page in paginator.paginate(Filters=filters):
       for reservation in page['Reservations']:
           instances.extend(reservation['Instances'])
          
   return instances

def get_instances_by_tags(tags: List[Dict[str, str]]) -> List[Dict[str, Any]]:
   ec2 = get_client()
   paginator = ec2.get_paginator('describe_instances')
   instances = []
  
   filters = [{"Name": f"tag:{t['Name']}", "Values": t['Values']} for t in tags]

   for page in paginator.paginate(Filters=filters):
       for reservation in page['Reservations']:
           instances.extend(reservation['Instances'])
          
   return instances