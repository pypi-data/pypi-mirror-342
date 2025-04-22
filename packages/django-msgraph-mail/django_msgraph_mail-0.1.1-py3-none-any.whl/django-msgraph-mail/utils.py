import time
import base64
import requests
from django.core.cache import cache


def get_access_token(client_id, client_secret, tenant_id):
    token = cache.get("msgraph_token")
    if token:
        return token

    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default"
    }

    response = requests.post(url, data=data)
    response.raise_for_status()
    token_data = response.json()
    access_token = token_data["access_token"]
    expires_in = token_data.get("expires_in", 3600)
    cache.set("msgraph_token", access_token, timeout=expires_in - 60)
    return access_token


def send_email(token, sender, recipients, subject, body, html_body=None, attachments=None):
    url = "https://graph.microsoft.com/v1.0/users/{}/sendMail".format(sender)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    message = {
        "subject": subject,
        "body": {
            "contentType": "HTML" if html_body else "Text",
            "content": html_body or body
        },
        "toRecipients": [
            {"emailAddress": {"address": addr}} for addr in recipients
        ]
    }

    if attachments:
        message["attachments"] = attachments

    payload = {"message": message, "saveToSentItems": "true"}

    res = requests.post(url, headers=headers, json=payload)
    res.raise_for_status()
