module "sandbox_endpoints" {
  source     = "../module/endpoints"
  vpc_id     = ""
  subnet_ids = ["", ""] #input private IP subnet
}
module "lambda" {
  source     = "../module/lambda"
  identifier = "identifier"

  secret_arn       = "" 
  ssh_username     = "ec2-user"
  target_tag_key = "RotateSSHKeys"
  target_tag_value = "True"

  vpc_id = "" 
}