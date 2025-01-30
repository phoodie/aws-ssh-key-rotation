variable "identifier" {
  description = "The identifier for the application"
  type        = string
}
variable "vpc_id" {
  description = "VPC ID where Lambda will be deployed"
  type        = string
}

variable "target_tag_key" {
  description = "Tag key for identifying target instances"
  type        = string
  default     = "Name"
}

variable "target_tag_value" {
  description = "Tag value for identifying target instances"
  type        = string
  default     = "ec2-al2023-pchau"
}

variable "ssh_username" {
  description = "SSH username for instances"
  type        = string
  default     = "ec2-user"
}

variable "secret_arn" {
  description = "Secret ARN of existing secret to use"
  type        = string
}