output "aws_security_group_lambda_sg_id" {
  description = "ID of the Lambda security group"
  value       = aws_security_group.lambda_sg.id
}