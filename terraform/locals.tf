locals {
  app_name_prefix = "aws-ssh-key-rotation"
  version         = file("${path.module}/VERSION.txt")
  default_tags = {
    module-name    = "aws-ssh-key-rotation"
    module-version = local.version
  }
}
