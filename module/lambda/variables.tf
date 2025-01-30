variable "identifier" {
  description = "The identifier for the application"
  type        = string
}
variable "vpc_id" {
  description = "VPC ID where Lambda will be deployed"
  type        = string
}

variable "secret_arn" {
  description = "Secret ARN of existing secret to use"
  type        = string
}