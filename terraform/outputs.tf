output "ecr_repository_url" {
  description = "URL of the repository"
  value       = aws_ecr_repository.this.repository_url
}
