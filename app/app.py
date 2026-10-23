import os
import json
import urllib.request
from flask import Flask, jsonify

app = Flask(__name__)
APP_NAME = os.getenv("APP_NAME", "AWS DevOps Demo")
DB_SECRET_ARN = os.getenv("DB_SECRET_ARN", "")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

def read_db_secret():
    if not DB_SECRET_ARN:
        return {"configured": False, "message": "DB_SECRET_ARN is not configured"}
    try:
        # Uses the EC2 instance profile; no static AWS keys are required.
        import boto3
        value = boto3.client("secretsmanager", region_name=AWS_REGION).get_secret_value(
            SecretId=DB_SECRET_ARN
        )
        secret = json.loads(value.get("SecretString", "{}"))
        return {
            "configured": True,
            "host": secret.get("host", ""),
            "username_present": bool(secret.get("username") or secret.get("username")),
            "password_present": bool(secret.get("password"))
        }
    except Exception as exc:
        # Avoid returning secret values or detailed credentials in HTTP responses.
        app.logger.warning("Unable to read database secret: %s", type(exc).__name__)
        return {"configured": True, "readable": False}

@app.get("/")
def home():
    secret_status = read_db_secret()
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>{APP_NAME}</title>
<style>body{{font:16px system-ui;max-width:760px;margin:60px auto;padding:0 20px;color:#182230}}
.card{{border:1px solid #d0d7de;border-radius:14px;padding:24px}}code{{background:#f1f5f9;padding:3px 6px;border-radius:5px}}</style>
</head><body><div class="card"><h1>{APP_NAME}</h1>
<p>Application is running behind the AWS load balancer.</p>
<ul><li>Health endpoint: <code>/health</code></li>
<li>Runtime: Flask + Gunicorn</li><li>Database secret configured: <b>{secret_status.get("configured")}</b></li></ul>
<p>Infrastructure is managed with Terraform. Do not expose database ports publicly.</p>
</div></body></html>"""

@app.get("/health")
def health():
    return jsonify(status="ok", app=APP_NAME), 200

@app.get("/db-secret-status")
def db_secret_status():
    # Returns status only; never exposes the secret or password.
    return jsonify(read_db_secret()), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
