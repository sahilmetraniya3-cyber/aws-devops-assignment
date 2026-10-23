output "application_https_url" {
  description = "ALB DNS name. Configure DNS for your domain to point here to use the ACM certificate hostname."
  value       = "https://${aws_lb.app.dns_name}"
}

output "alb_dns_name" {
  value = aws_lb.app.dns_name
}

output "rds_endpoint" {
  value = aws_db_instance.main.address
}

output "alb_logs_bucket" {
  value = aws_s3_bucket.alb_logs.bucket
}

output "vpc_id" {
  value = aws_vpc.main.id
}
