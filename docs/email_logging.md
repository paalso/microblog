# Email Error Logging Setup Guide for Flask Applications

This document explains how to configure **automatic error reporting via email** in a Flask application. When enabled, the application will send email notifications whenever an unhandled exception or logged error (level `ERROR` or higher) occurs in production.

---

## 1. Overview

Email-based error logging is a classic monitoring technique for web applications. Instead of relying solely on log files or external services, your Flask application can notify administrators directly via email when something goes wrong.

This guide covers:

- configuring SMTP email settings (including Gmail)
- integrating an email logging handler
- production-only activation
- testing and troubleshooting

---

## 2. Environment Variables (`.env`)

Add the following variables to your project `.env` file:

```env
# ------------------------------
# Email settings
# ------------------------------
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=your@gmail.com
MAIL_PASSWORD=twhodukatmlibseh
ADMINS=admin1@example.com,admin2@example.com
```

### Important notes

- MAIL_PASSWORD must be written **without spaces and without quotes**, even though Google shows it as "xxxx xxxx xxxx xxxx".

- ADMINS is a comma-separated list of recipient email addresses.

- Emails will be sent from **MAIL_USERNAME** to all addresses listed in **ADMINS**.

## 3. Create Google App Password (Gmail Only)

Because Google disables SMTP access using normal passwords, you must create an App Password.

Steps:

1. Go to Google Account → Security

2. Enable 2-Step Verification (required)

3. Open App passwords

4. Create a new password for application:

   → Choose “Mail”

   → Name it “Flask” or anything you want

5. Google will display a 16-character password: `xxxx xxxx xxxx xxxx`

Use the same characters without spaces as your MAIL_PASSWORD.

## 4. Configuring Flask Error Email Logging

Create a module:
```
app/email_logging.py
```

Contents:
```
import logging
from logging.handlers import SMTPHandler

def configure_email_errors(app):
    """Configure email-based error logging for production."""
    if app.debug:
        return  # skip in development mode

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
```

## 5. Integrating With `create_app()`

Inside app/__init__.py:
```
from app.email_logging import configure_email_errors

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    configure_logging(app)
    configure_email_errors(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    from app.errors import errors_bp
    app.register_blueprint(errors_bp)

    return app
```

This will attach the email handler immediately after regular logging is set up.

## 6. What Errors Generate Emails?

The email handler sends notifications when:

- An **unhandled exception** occurs in a request.

- Flask logs an error via `app.logger.error(...)`.

- Any component (database engine, extension, etc.) emits a log message with level:

  - `ERROR`

  - `CRITICAL`

Emails will **not** be sent during development (`app.debug = True`).

## 7. Testing the Setup

### Option A — trigger an error manually

Create a temporary test route:

```
@app.route('/test_error')
def test_error():
    app.logger.error("Test error email")
    return "Error triggered"
```

Access /test_error while Flask runs in production mode:

```
FLASK_ENV=production flask run
```

### Option B — trigger an actual exception

```
@app.route('/boom')
def boom():
    1 / 0
```

This will generate a traceback and send an email.

## 8. Common Problems & Solutions

### "Authentication failed"

  - You entered the Gmail password incorrectly

  - You used your normal Google password instead of an App Password

  - App Password not copied correctly (remove spaces!)

### Emails don't arrive

  - The app is running in debug mode

  - SMTP port blocked by hosting

  - ADMINS not parsed correctly (missing .split(",") in config)

### Gmail blocks the sign-in

  - Check your inbox or Google Security alerts
  ("Was this you?")

  - Confirm the sign-in attempt

## 9. Best Practices

- Enable email logging only in production.

- Never commit real credentials; use .env + .gitignore.

- Use multiple admin emails for redundancy.

- Combine with file logging for full diagnostics.

## 10. Recommended File Structure

```
project/
    app/
        __init__.py
        email_logging.py
        logging_config.py
        routes.py
        errors.py
    docs/
        email_logging.md   <-- place this guide here
    .env
    README.md
```

## ✔ Summary

With Gmail App Passwords and a simple SMTPHandler, Flask can automatically email you whenever an error occurs in production. This provides a lightweight, reliable monitoring mechanism without external services.
