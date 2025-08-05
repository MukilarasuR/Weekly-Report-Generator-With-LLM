import requests
import json
from msal import ConfidentialClientApplication
import os

TENANT_ID = os.getenv("OUTLOOK_TENANT_ID")
CLIENT_ID = os.getenv("OUTLOOK_CLIENT_ID")
CLIENT_SECRET = os.getenv("OUTLOOK_CLIENT_SECRET")
SENDER_EMAIL = os.getenv("OUTLOOK_SENDER_EMAIL")  # sender must match registered account

def get_access_token():
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET
    )

    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" not in result:
        raise Exception("Failed to obtain Outlook access token")
    return result["access_token"]

def send_outlook_email(to: str, subject: str, body: str):
    access_token = get_access_token()
    url = f"https://graph.microsoft.com/v1.0/users/{SENDER_EMAIL}/sendMail"

    email_msg = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": to
                    }
                }
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(email_msg))
    if response.status_code != 202:
        raise Exception(f"Failed to send email via Outlook: {response.text}")