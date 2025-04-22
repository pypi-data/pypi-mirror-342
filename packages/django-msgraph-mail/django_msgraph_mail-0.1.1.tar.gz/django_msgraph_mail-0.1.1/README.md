# django-msgraph-mail

A Django email backend for sending emails via the Microsoft Graph API. This package integrates seamlessly with Django's built-in email system, allowing you to send emails using Microsoft 365 accounts.

## Features
- Simple integration with Django's email framework.
- Secure email delivery using Microsoft Graph API.
- Supports all standard Django email functions.

## Prerequisites
Before installing and configuring `django-msgraph-mail`, ensure you have:
- A Django project (version 3.2 or higher recommended).
- A Microsoft 365 account with email capabilities.
- An Azure Active Directory (AAD) application registered with the following:
  - `Mail.Send` permission under Microsoft Graph API (Application permissions).
  - A client secret generated for the application.
  - Access to the Tenant ID, Client ID, and Client Secret.

## Installation
Install the package using pip:

```bash
pip install django-msgraph-mail
```

## Configuration
To configure the email backend, add the following settings to your Django project's `settings.py` file:

```python
EMAIL_BACKEND = "django_msgraph_mail.backend.GraphEmailBackend"
EMAIL_SENDER = "your-sender@domain.com"
CLIENT_ID = "your-azure-client-id"
CLIENT_SECRET = "your-azure-client-secret"
TENANT_ID = "your-tenant-id"
```

### Configuration Details
- **`EMAIL_SENDER`**: The email address of the Microsoft 365 account used to send emails (e.g., `sender@yourdomain.com`).
- **`CLIENT_ID`**: The Application (client) ID of your Azure AD app.
- **`CLIENT_SECRET`**: A secret key generated for your Azure AD app.
- **`TENANT_ID`**: The Directory (tenant) ID of your Azure AD.

#### Security Recommendation
Store sensitive information like `CLIENT_SECRET` in environment variables to avoid exposing them in your codebase. Example:

```python
import os

CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
```

#### Setting Up Azure AD
1. Go to the [Azure Portal](https://portal.azure.com) and sign in.
2. Navigate to **Azure Active Directory** > **App registrations** > **New registration**.
3. Register an application and note the **Application (client) ID** and **Directory (tenant) ID**.
4. Under **Certificates & secrets**, create a new client secret and copy its value.
5. Under **API permissions**, add the `Mail.Send` permission for Microsoft Graph (Application permissions) and grant admin consent.

## Usage
Once configured, you can use Django's built-in email functions to send emails. Example:

```python
from django.core.mail import send_mail

send_mail(
    subject="Welcome to My App",
    message="Thank you for signing up!",
    from_email="sender@yourdomain.com",
    recipient_list=["recipient@example.com"],
    fail_silently=False,
)
```

### Additional Examples
#### Sending HTML Emails
```python
from django.core.mail import EmailMultiAlternatives

email = EmailMultiAlternatives(
    subject="HTML Email",
    body="This is a plain text version.",
    from_email="sender@yourdomain.com",
    to=["recipient@example.com"],
)
email.attach_alternative("<p>This is an <b>HTML</b> email!</p>", "text/html")
email.send(fail_silently=False)
```

#### Sending to Multiple Recipients
```python
send_mail(
    subject="Newsletter",
    message="Here's the latest news!",
    from_email="sender@yourdomain.com",
    recipient_list=["user1@example.com", "user2@example.com"],
    fail_silently=False,
)
```

## Troubleshooting
- **Authentication Errors**: Verify that `CLIENT_ID`, `CLIENT_SECRET`, and `TENANT_ID` are correct. Ensure the Azure AD app has the `Mail.Send` permission and admin consent.
- **Emails Not Sending**: Check that the `EMAIL_SENDER` matches the Microsoft 365 account or a valid alias. Ensure the account has a valid license.
- **Network Issues**: Confirm your server can access `https://graph.microsoft.com`.
- **Debugging**: Set `fail_silently=False` to raise exceptions and check Django logs for detailed error messages.

## Contributing
Contributions are welcome! Please submit issues or pull requests to the [GitHub repository](https://github.com/TheodoreAsher/django-msgraph-mail).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support
For questions or support, open an issue on the [GitHub repository](https://github.com/TheodoreAsher/django-msgraph-mail) or contact [django.infusion@gmail.com].