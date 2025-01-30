resource "aws_ecr_repository" "this" {
  name                 = local.app_name_prefix
  image_tag_mutability = "IMMUTABLE"
  force_delete         = true
}

# Testing this container within lz infra sandbox
# data "aws_iam_policy_document" "ecr_access_policy" {
#   statement {
#     sid    = "AllowOrganizationAccess"
#     effect = "Allow"

#     principals {
#       type        = "AWS"
#       identifiers = ["*"]
#     }

#     condition {
#       test     = "StringEquals"
#       variable = "aws:PrincipalOrgID"
#       values   = [data.aws_organizations_organization.this.id]
#     }

#     actions = [
#       "ecr:BatchGetImage",
#       "ecr:GetDownloadUrlForLayer"
#     ]
#   }

#   statement {
#     sid    = "CrossAccountPermission"
#     effect = "Allow"
#     actions = [
#       "ecr:BatchGetImage",
#       "ecr:GetDownloadUrlForLayer"
#     ]

#     principals {
#       type        = "Service"
#       identifiers = ["lambda.amazonaws.com"]
#     }

#     condition {
#       test     = "StringEquals"
#       variable = "aws:SourceOrgID"
#       values   = [data.aws_organizations_organization.this.id]
#     }
#   }
# }

# resource "aws_ecr_repository_policy" "this" {
#   repository = aws_ecr_repository.this.name
#   policy     = data.aws_iam_policy_document.ecr_access_policy.json
# }

resource "docker_image" "this" {
  name = "${aws_ecr_repository.this.repository_url}:${local.version}"

  build {
    context  = "../function"
    platform = "linux/amd64"
    no_cache = true
  }
}

resource "docker_registry_image" "this" {
  name          = docker_image.this.name
  keep_remotely = true
}