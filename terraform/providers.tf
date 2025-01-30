terraform {
  required_version = ">= 1.9"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.7"
    }

    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }

    archive = {
      source  = "hashicorp/archive"
      version = "2.6.0"
    }
  }

  backend "s3" {
    encrypt = true
    region  = "ap-southeast-2"
  }
}

provider "aws" {
  region = "ap-southeast-2"

  default_tags {
    tags = {
      deployed_from       = "phoodie/aws-ssh-key-rotation"
      deployed_using      = "terraform"
      repository_template = "terraform-template"
      app                 = local.app_name_prefix
      version             = local.version
    }
  }
}

data "aws_ecr_authorization_token" "this" {}

provider "docker" {
  registry_auth {
    address  = data.aws_ecr_authorization_token.this.proxy_endpoint
    username = data.aws_ecr_authorization_token.this.user_name
    password = data.aws_ecr_authorization_token.this.password
  }
}
