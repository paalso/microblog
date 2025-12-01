from .console_logging import configure_console_logging
from .email_logging import configure_email_errors
from .file_logging import configure_file_logging


def init_logging(app):
    """Initialize all logging handlers."""
    app.logger.handlers.clear()

    configure_console_logging(app)
    configure_email_errors(app)
    configure_file_logging(app)

    # Email logging should be active only in production
    if not app.debug and not app.testing:
        configure_email_errors(app)
