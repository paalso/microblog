import logging
from logging import StreamHandler


def configure_logging(app):
    if any(isinstance(h, StreamHandler) for h in app.logger.handlers):
        return

    app.logger.setLevel(logging.DEBUG)

    console_handler = StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)
