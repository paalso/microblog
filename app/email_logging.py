import logging
from logging.handlers import SMTPHandler


def configure_email_errors(app):
    """Configure email-based error logging in production."""
    if app.debug:
        return  # do nothing in development

    mail_server = app.config.get('MAIL_SERVER')
    if not mail_server:
        return

    auth = None
    username = app.config.get('MAIL_USERNAME')
    password = app.config.get('MAIL_PASSWORD')
    if username or password:
        auth = (username, password)

    secure = None
    if app.config.get('MAIL_USE_TLS'):
        secure = ()

    mail_handler = SMTPHandler(
        mailhost=(mail_server, app.config.get('MAIL_PORT')),
        fromaddr=f"no-reply@{mail_server}",
        toaddrs=app.config.get('ADMINS'),
        subject='Application Error',
        credentials=auth,
        secure=secure
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
