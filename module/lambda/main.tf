resource "aws_cloudwatch_log_group" "this" {
  name              = "phoodie/ssh-key-rotation/${var.identifier}"
  retention_in_days = 30
  tags              = local.default_tags
}

resource "aws_lambda_function" "this" {
  function_name = local.app_name
  role          = aws_iam_role.function.arn
  package_type  = "Image"
  image_uri     = "${local.aws_account_id}.dkr.ecr.ap-southeast-2.amazonaws.com/aws-ssh-key-rotation:${local.version}"
  timeout       = 300
  ## try excluding this when deploy in sharedservices
  vpc_config {
    security_group_ids = [aws_security_group.lambda_sg.id]
    subnet_ids         = data.aws_subnets.private.ids
  }
  ##
  environment {
    variables = {
      TAGNAME        = var.target_tag_key
      TAGVALUE       = var.target_tag_value
      USERNAME       = var.ssh_username
      SNSARN         = local.sns_topic_arn
      SSMROLE       = aws_iam_role.ssm_notification.arn
      MODULE_VERSION = local.version
    }
  }
  logging_config {
    log_group  = aws_cloudwatch_log_group.this.name
    log_format = "JSON"
  }
  tags = local.default_tags
}

resource "aws_secretsmanager_secret_rotation" "this" {
  secret_id = var.secret_arn
  rotation_lambda_arn = local.rotation_lambda_arn

  rotation_rules {
    automatically_after_days = 30
  }
}