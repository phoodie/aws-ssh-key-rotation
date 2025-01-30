## AWS SSH Key Rotation

Terraform module, where you just need to provide a secret arn, and this module will take care of deploying:

Lambda -> To perform the SSH Key rotation on instances
Secrets -> populates it with private and public key & enables rotation
Cloudwatch -> to watch the activity log of the lambda activity
Entity -> Audit trail purposes


The purpose of this is to meet best security practices of not using static ssh keys, but instead to use dynamic ssh keys, preventing the threat of ssh keys being compromised.