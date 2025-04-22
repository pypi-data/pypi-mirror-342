from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
from .utils import get_access_token, send_email


class GraphEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        client_id = settings.CLIENT_ID
        client_secret = settings.CLIENT_SECRET
        tenant_id = settings.TENANT_ID
        sender = settings.EMAIL_SENDER

        token = get_access_token(client_id, client_secret, tenant_id)
        sent_count = 0

        for msg in email_messages:
            recipients = list(msg.to)
            subject = msg.subject
            body = msg.body
            html_body = None
            attachments = []

            if hasattr(msg, 'alternatives'):
                for alt in msg.alternatives:
                    if alt[1] == 'text/html':
                        html_body = alt[0]

            if msg.attachments:
                for attachment in msg.attachments:
                    if isinstance(attachment, tuple):
                        filename, content, mimetype = attachment
                        attachments.append({
                            "@odata.type": "#microsoft.graph.fileAttachment",
                            "name": filename,
                            "contentBytes": content.encode("base64"),
                            "contentType": mimetype
                        })

            send_email(token, sender, recipients, subject, body, html_body, attachments)
            sent_count += 1

        return sent_count
