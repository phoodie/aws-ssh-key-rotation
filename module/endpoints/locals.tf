locals {
  services = {
    secretsmanager = "com.amazonaws.ap-southeast-2.secretsmanager"
    ssm            = "com.amazonaws.ap-southeast-2.ssm"
    ssmmessages    = "com.amazonaws.ap-southeast-2.ssmmessages"
    ec2messages    = "com.amazonaws.ap-southeast-2.ec2messages"
    ecr_api        = "com.amazonaws.ap-southeast-2.ecr.api"
    ecr-dr         = "com.amazonaws.ap-southeast-2.ecr.dkr"
    ec2            = "com.amazonaws.ap-southeast-2.ec2"
  }
}