resource "aws_vpc_endpoint" "endpoints" {
  for_each = local.services

  vpc_id              = var.vpc_id
  service_name        = each.value
  vpc_endpoint_type   = "Interface"
  subnet_ids          = var.subnet_ids
  security_group_ids  = [aws_security_group.endpoint_sg[each.key].id]
  private_dns_enabled = true

  tags = merge(
    var.tags,
    {
      Name          = "vpc-endpoint-${each.key}"
    }
  )
}