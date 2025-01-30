# START SSM Notification Role & Policies
data "aws_iam_policy_document" "assume_ssm_notification_role" {
 statement {
   sid     = "AllowSSMToAssumeRole"
   effect  = "Allow"
   actions = ["sts:AssumeRole"]
   principals {
     type = "Service" 
     identifiers = ["ssm.amazonaws.com"]
   }
 }
}

resource "aws_iam_role" "ssm_notification" {
 name               = "${local.app_name}-ssm-notification"
 assume_role_policy = data.aws_iam_policy_document.assume_ssm_notification_role.json
 tags               = local.default_tags
}

data "aws_iam_policy_document" "ssm_notifications" {
 statement {
   sid    = "AllowSNSAndRoleOperations"
   effect = "Allow" 
   actions = [
     "sns:Publish",
     "iam:GetRole",
     "iam:PassRole"
   ]
   resources = [
     local.sns_topic_arn,
     aws_iam_role.ssm_notification.arn
   ]
 }
}

resource "aws_iam_policy" "ssm_notifications" {
 name        = "${local.app_name}-ssm-notifications"
 description = "Policy for SSM notifications"
 policy      = data.aws_iam_policy_document.ssm_notifications.json
 tags        = local.default_tags
}

resource "aws_iam_role_policy_attachments_exclusive" "ssm_notification_role" {
 role_name = aws_iam_role.ssm_notification.name
 policy_arns = [aws_iam_policy.ssm_notifications.arn]
}
# END SSM Notification Role & Policies

# Lambda Role & Policies
data "aws_iam_policy_document" "assume_lambda_role" {
 statement {
   sid     = "AllowLambdaToAssumeRole"
   effect  = "Allow"
   actions = ["sts:AssumeRole"]
   principals {
     type = "Service"
     identifiers = ["lambda.amazonaws.com"]
   }
 }
}

resource "aws_iam_role" "function" {
 name               = "${local.app_name}-function"
 assume_role_policy = data.aws_iam_policy_document.assume_lambda_role.json
 tags               = local.default_tags
}

data "aws_iam_policy_document" "lambda_secrets" {
 statement {
   sid    = "AllowSecretsManagerOperations"
   effect = "Allow"
   actions = [
     "secretsmanager:GetSecretValue",
     "secretsmanager:DescribeSecret", 
     "secretsmanager:PutSecretValue",
     "secretsmanager:UpdateSecretVersionStage",
     "secretsmanager:CreateSecret",
     "secretsmanager:RotateSecret"
   ]
   resources = [var.secret_arn]
 }
}

resource "aws_iam_policy" "lambda_secrets" {
 name        = "${local.app_name}-secrets"
 description = "Policy to allow lambda to access secrets manager"
 policy      = data.aws_iam_policy_document.lambda_secrets.json
 tags        = local.default_tags
}

data "aws_iam_policy_document" "lambda_ssm" {
 statement {
   sid    = "AllowSSMOperations"
   effect = "Allow"
   actions = [
     "ssm:SendCommand",
     "ssm:GetCommandInvocation",
     "ssm:ListCommands", 
     "ssm:ListCommandInvocations",
     "ssm:DescribeInstanceInformation",
     "sns:Publish",
     "iam:PassRole"
   ]
   resources = ["*"] 
 }
}

resource "aws_iam_policy" "lambda_ssm" {
 name        = "${local.app_name}-ssm"
 description = "Policy to allow lambda to execute SSM commands"
 policy      = data.aws_iam_policy_document.lambda_ssm.json
 tags        = local.default_tags
}

resource "aws_iam_role_policy_attachments_exclusive" "function_execution_role" {
  role_name = aws_iam_role.function.name
  policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole",
    "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess",
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    "arn:aws:iam::aws:policy/SecretsManagerReadWrite",
    aws_iam_policy.lambda_ssm.arn,
    aws_iam_policy.ssm_notifications.arn #SNS & SSM
  ]
}

resource "aws_lambda_permission" "secretsmanager" {
  statement_id  = "AllowSecretsManagerInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "secretsmanager.amazonaws.com"
}