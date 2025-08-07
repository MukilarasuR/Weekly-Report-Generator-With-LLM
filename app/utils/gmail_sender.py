import os
import base64
import pickle
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes for sending Gmail
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Paths to store token & credentials
TOKEN_PATH = "app/utils/token.pickle"
CREDENTIALS_PATH = "app/utils/credentials.json"

def get_gmail_service():
    creds = None

    # 🔁 Reuse token if already available
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token_file:
            creds = pickle.load(token_file)

    # 🔐 Refresh or re-authenticate if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        # 💾 Save new token for reuse
        with open(TOKEN_PATH, "wb") as token_file:
            pickle.dump(creds, token_file)

    service = build("gmail", "v1", credentials=creds)
    return service

def send_email(to, subject, body):
    service = get_gmail_service()

    message = MIMEText(body, "plain")
    message["to"] = to
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    send_body = {"raw": raw_message}

    service.users().messages().send(userId="me", body=send_body).execute()
