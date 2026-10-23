# AWS Infrastructure & CI/CD — DevOps Practical Assignment

A Terraform-based demonstration project for a two-AZ AWS VPC, public ALB with HTTPS, private EC2 Auto Scaling Group, private RDS MySQL, Secrets Manager, IAM instance role, S3 ALB access logs, and GitHub Actions CI/CD.

> **Important:** This is a starter implementation, not proof of a successful deployment. Review the Terraform and AWS costs before applying. The sample application is intentionally lightweight. It exposes `/health`; the database secret integration is demonstrated in the companion Flask source under `app/`, while the EC2 user-data app is a minimal health-check demo.

## Architecture

Internet → HTTPS ALB → EC2 Auto Scaling Group → private RDS MySQL  
ALB → S3 access logs  
EC2 instance profile → Secrets Manager (scoped read access)

See `docs/architecture.mmd` for a Mermaid diagram source.

## Prerequisites

- AWS account with permissions to create VPC, EC2, ELB, RDS, IAM, S3, Secrets Manager, and ACM resources.
- AWS CLI v2, Terraform >= 1.6, Git.
- An ACM certificate in the same region as the ALB, validated for a hostname you control.
- Current Amazon Linux 2023 AMI ID for your chosen region.
- GitHub repository and GitHub Actions enabled.

## 1. Configure AWS credentials locally

Use an IAM role or AWS CLI profile where possible. Avoid root credentials.

```bash
aws configure --profile devops-assignment
export AWS_PROFILE=devops-assignment
aws sts get-caller-identity
```

For a shared or production environment, use short-lived credentials/roles rather than static access keys.

## 2. Prepare certificate and AMI

Request/validate an ACM certificate for your domain in `ap-south-1` (or the region you choose). You need control of DNS to complete validation. An ALB DNS name by itself will not match a certificate for your custom domain.

Find a current Amazon Linux 2023 AMI from AWS Systems Manager public parameters or the EC2 console. Do not use the placeholder AMI ID.

## 3. Configure Terraform variables safely

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` and set `ami_id` and `certificate_arn`. Do not put a real database password in the file. Export a strong password in your shell:

```bash
export TF_VAR_db_password='REPLACE_WITH_A_LONG_RANDOM_PASSWORD'
terraform init
terraform fmt -recursive
terraform validate
terraform plan
```

Review the plan and estimated costs. Then deploy:

```bash
terraform apply
```

Capture outputs:

```bash
terraform output
```

## 4. DNS and HTTPS

Create a DNS `A/AAAA` alias (Route 53) or supported CNAME record for your hostname pointing to the ALB. The certificate must cover the hostname. Do not claim the ALB HTTPS endpoint works with a certificate for a different domain.

## 5. GitHub Actions setup

Configure GitHub repository variables:
- `AWS_REGION` — e.g. `ap-south-1`
- `AMI_ID` — current Amazon Linux 2023 AMI ID
- `CERTIFICATE_ARN` — validated ACM certificate ARN

Configure GitHub repository/environment secrets:
- `AWS_ROLE_ARN` — IAM role trusted for this GitHub repository/environment via OIDC
- `DB_PASSWORD` — strong database password

Set up AWS IAM OIDC provider and a role trust policy restricted to the repository and `main` branch/environment. Grant only the permissions needed by the Terraform resources. The workflow applies on pushes to `main` that change Terraform and on manual dispatch; use GitHub environment approval and split plan/apply for stricter controls.

**Terraform state:** This starter uses local state by default. For team/CI use, configure a remote S3 backend with encryption, versioning, and a locking strategy supported by your Terraform version. Do not run concurrent applies against separate local states.

## 6. Test

```bash
curl -i https://YOUR_DOMAIN/health
```

Expected response: HTTP 200 with JSON status `ok`.

Also check:
- Target group reports healthy EC2 targets.
- RDS is not publicly accessible.
- DB security group allows 3306 only from the application security group.
- S3 bucket public access block is enabled and ALB logs are delivered.
- No secrets are present in Git history or screenshots.

## 7. Deliverables checklist

- [ ] GitHub repository with source code and Terraform
- [ ] GitHub Actions workflow and OIDC configuration notes
- [ ] Architecture diagram
- [ ] `terraform plan` and deployment screenshots
- [ ] Successful `/health` response screenshot
- [ ] README with prerequisites, deployment and cleanup
- [ ] Working HTTPS URL using your validated domain
- [ ] Evidence of private RDS and restricted security groups

## 8. Cleanup — avoid ongoing charges

After you have captured evidence and no longer need the environment:

```bash
cd terraform
terraform destroy
```

Review the plan before confirming. The S3 logs bucket is configured with `force_destroy = true` for this disposable assignment, so its contents can be deleted during destroy. Do not use this setting for production log retention.

## Notes / known limitations to review before applying

- NAT Gateway, ALB, RDS and EC2 incur costs while running. Set AWS Budgets alerts first.
- One NAT Gateway is used to reduce cost; it is not fully AZ-resilient. Production high availability commonly uses one NAT Gateway per AZ.
- The included EC2 user-data app is a minimal Python HTTP health-check demo, not the Flask app under `app/`. To deploy the Flask app, build/publish its container or configure a proper artifact deployment pipeline and update the Launch Template.
- Database credentials are managed by Secrets Manager, but Terraform state can still contain sensitive values. Protect the state file and use a remote encrypted backend with restricted access.
- RDS password rotation is not configured.
- Validate provider/API compatibility and the ALB log bucket policy for your chosen region before deployment.
- This is an assessment starter, not a production-hardened reference architecture.
