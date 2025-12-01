import logging
import os
from logging.handlers import RotatingFileHandler


def configure_file_logging(app):
    """Setup rotating file logging."""
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    file_handler = RotatingFileHandler(
        f'{log_dir}/microblog.log',
        maxBytes=10240,     # 10 KB
        backupCount=10
    )

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
