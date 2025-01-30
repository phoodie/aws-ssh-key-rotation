locals {
  common_tags = {
    Environment = "experimental"
    ManagedBy   = "pchau"
    Purpose     = "SSH-Key-Rotation-Testing"
  }
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.selected.id]
  }

  filter {
    name   = "tag:Name"
    values = ["*private*"]
  }
}

#deploy ec2 for test

# Get a private subnet for the EC2 instance
data "aws_subnet" "private" {
  id = data.aws_subnets.private.ids[0]
}

data "aws_iam_instance_profile" "this" {
  name = "SSM"
}

# EC2 instance for testing
resource "aws_instance" "test" {
  ami                    = ""
  instance_type          = "t3.micro"
  subnet_id              = data.aws_subnet.private.id
  vpc_security_group_ids = [""]
  iam_instance_profile   = data.aws_iam_instance_profile.this.name
  # key_name               = ""

  tags = local.common_tags
}
