import logging
from logging import StreamHandler


def configure_console_logging(app):
    """Setup console logging."""
    app.logger.setLevel(logging.DEBUG)

    handler = StreamHandler()
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
