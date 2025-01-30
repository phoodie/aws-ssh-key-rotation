variable "secret_arn" {
  description = "ARN of the secret in Secrets Manager"
  type        = string
}

variable "target_tag_key" {
  description = "Tag key to identify instances to rotate keys for"
  type        = string
  default     = "Name"
}

variable "target_tag_value" {
  description = "Tag value to identify instances to rotate keys for"
  type        = string

}

variable "ssh_username" {
  description = "SSH username for the EC2 instances"
  type        = string
  default     = "ec2-user"

}

variable "vpc_id" {
  description = "VPC ID to create the security group in"
  type        = string

}