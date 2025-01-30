locals {
  version                   = file("${path.module}/VERSION.txt")
  aws_account_id = ""
  app_name                  = "${var.identifier}-ssh-key-rotation"
  rotation_lambda_arn       = "arn:aws:lambda:ap-southeast-2:${local.aws_account_id}:function:${local.app_name}" 
  sns_topic_arn       = "" 

  default_tags = {
    module-name         = "aws-ssh-key-rotation"
    module-version = local.version
  }
}
