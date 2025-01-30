# TFLint configuration options: https://github.com/terraform-linters/tflint/blob/423e0c4c1ea19c8506ac6b78049f460781633800/docs/user-guide/config.md

tflint {
  required_version = ">= 0.50"
}

config {
}

plugin "aws" {
  enabled = true
  version = "0.32.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}
