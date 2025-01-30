# all this should be hashed 
resource "aws_security_group" "lambda_sg" {
  name        = "${local.app_name}-lambda"
  description = "Security group for lambda SSH key rotation"
  vpc_id      = var.vpc_id
  tags = merge(local.default_tags, {
    Name          = "${local.app_name}-lambda"
  })
}

resource "aws_security_group" "target_sg" {
  name        = "${local.app_name}-target"
  description = "Security group for target instances"
  vpc_id      = var.vpc_id
  tags = merge(local.default_tags, {
    Name          = "${local.app_name}-target"
  })
}

resource "aws_vpc_security_group_egress_rule" "lambda_to_target" {
  security_group_id            = aws_security_group.lambda_sg.id
  referenced_security_group_id = aws_security_group.target_sg.id
  from_port                    = 22
  to_port                      = 22
  ip_protocol                  = "tcp"
  description                  = "Allow SSH to target instances"
}

resource "aws_vpc_security_group_ingress_rule" "target_from_lambda" {
  security_group_id            = aws_security_group.target_sg.id
  referenced_security_group_id = aws_security_group.lambda_sg.id
  from_port                    = 22
  to_port                      = 22
  ip_protocol                  = "tcp"
  description                  = "Allow SSH access from Lambda rotation function"
}

# allow lambda to reach vpc endpoints secretsmanager and ssm
resource "aws_security_group_rule" "lambda_to_vpc_endpoints" {
  type              = "egress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["10.0.0.0/16"]
  security_group_id = aws_security_group.lambda_sg.id
}

## this was needed for lambda to reach endpoint 22
resource "aws_security_group_rule" "lambda_to_nat" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]  # For NAT Gateway access
  security_group_id = aws_security_group.lambda_sg.id
}