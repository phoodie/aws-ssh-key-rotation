variable "vpc_id" {
  description = "ID of the VPC where endpoints will be created"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs where endpoints will be created"
  type        = list(string)
}

# variable "lambda_security_group_id" {
#   description = "ID of the Lambda security group that needs access to the VPC endpoints"
#   type        = string
# }

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}