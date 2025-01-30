# resource "aws_security_group" "endpoint_sg" {
#   for_each    = local.services
#   name        = "vpc-endpoint-${each.key}"
#   description = "Security group for ${each.key} VPC endpoint"
#   vpc_id      = var.vpc_id
#   tags = merge(
#     var.tags,
#     {
#       Name          = "vpc-endpoint-${each.key}"
#     }
#   )
# }

# # Allow all VPC CIDR to access endpoints
# resource "aws_vpc_security_group_ingress_rule" "endpoints_from_vpc" {
#   for_each          = local.services
#   security_group_id = aws_security_group.endpoint_sg[each.key].id
#   cidr_ipv4         = "10.0.0.0/16"
#   from_port         = 443
#   to_port           = 443
#   ip_protocol       = "tcp"
#   description       = "Allow HTTPS from VPC CIDR"
# }

# # lambda specific security group
# resource "aws_vpc_security_group_egress_rule" "lambda_to_endpoints" {
#   for_each                     = local.services
#   security_group_id            = var.lambda_security_group_id
#   referenced_security_group_id = aws_security_group.endpoint_sg[each.key].id
#   from_port                    = 443
#   to_port                      = 443
#   ip_protocol                  = "tcp"
#   description                  = "Allow Lambda to connect to ${each.key} endpoint"
# }

resource "aws_security_group" "lambda_sg" {
  name        = "lambda-sg"
  description = "Security group for Lambda functions"
  vpc_id      = var.vpc_id
  tags = merge(
    var.tags,
    {
      Name          = "lambda-sg"
    }
  )
}

resource "aws_security_group" "endpoint_sg" {
  for_each    = local.services
  name        = "vpc-endpoint-${each.key}"
  description = "Security group for ${each.key} VPC endpoint"
  vpc_id      = var.vpc_id
  tags = merge(
    var.tags,
    {
      Name          = "vpc-endpoint-${each.key}"
    }
  )
}

# Allow all VPC CIDR to access endpoints
resource "aws_vpc_security_group_ingress_rule" "endpoints_from_vpc" {
  for_each          = local.services
  security_group_id = aws_security_group.endpoint_sg[each.key].id
  cidr_ipv4         = "10.0.0.0/16"
  from_port         = 443
  to_port           = 443
  ip_protocol          = "tcp"
  description       = "Allow HTTPS from VPC CIDR"
}

# Allow Lambda to connect to endpoints
resource "aws_vpc_security_group_egress_rule" "lambda_to_endpoints" {
  for_each                     = local.services
  security_group_id            = aws_security_group.lambda_sg.id
  referenced_security_group_id = aws_security_group.endpoint_sg[each.key].id
  from_port                    = 443
  to_port                      = 443
  ip_protocol                  = "tcp"
  description                  = "Allow Lambda to connect to ${each.key} endpoint"
}
