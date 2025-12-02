
from flask import current_app
from flask_mail import Message

from app import mail


def send_email(subject, sender, recipients, text_body, html_body=None):
    """Send an email using Flask-Mail."""
    msg = Message(
        subject,
        sender=sender,
        recipients=recipients
    )
    msg.body = text_body

    if html_body:
        msg.html = html_body

    try:
        mail.send(msg)
        current_app.logger.info(f"📧 Email sent to {recipients}: {subject}")
    except Exception as e:
        current_app.logger.error(f"❌ Failed to send email: {e}")
