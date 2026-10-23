# Submission Checklist

## Evidence to capture (real screenshots only)
1. Terraform `validate` successful output.
2. Terraform apply completed and outputs.
3. VPC showing two AZs and subnet layout.
4. ALB listener HTTPS:443 and healthy target group.
5. EC2 Auto Scaling Group with two instances.
6. RDS showing Public access = No and encrypted storage.
7. Secrets Manager secret metadata (never reveal the secret value).
8. S3 bucket public access block and delivered ALB logs.
9. GitHub Actions successful workflow run.
10. Browser showing `https://YOUR_DOMAIN/health` returning HTTP 200.

## Before sending to HR
- Replace all placeholders.
- Ensure the URL is live and tested from a separate network/browser.
- Remove passwords, tokens, account IDs if not required, and sensitive console data from screenshots.
- Add a short explanation of trade-offs and costs to README.
- Never submit fabricated screenshots or claim uncompleted work is deployed.
