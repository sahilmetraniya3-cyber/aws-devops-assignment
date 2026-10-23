variable "aws_region" {
  description = "AWS region for all resources."
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  type    = string
  default = "devops-assignment"
}

variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "ami_id" {
  description = "Amazon Linux 2023 AMI ID for the selected region. Look up a current AMI before applying."
  type        = string
}

variable "certificate_arn" {
  description = "ACM certificate ARN in the same region as the ALB. Certificate must cover the hostname."
  type        = string
}

variable "app_port" {
  type    = number
  default = 8080
}

variable "db_name" {
  type    = string
  default = "appdb"
}

variable "db_username" {
  type      = string
  default   = "appuser"
  sensitive = true
}

variable "db_password" {
  description = "Use a strong temporary password. Prefer setting TF_VAR_db_password in the shell/CI secret store; do not commit it."
  type        = string
  sensitive   = true
}

variable "enable_nat_gateway" {
  description = "NAT Gateway costs money. Keep true for private EC2 outbound access; set false only if you intentionally change the architecture."
  type        = bool
  default     = true
}
