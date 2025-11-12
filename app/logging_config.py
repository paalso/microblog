import logging
import os
from logging.handlers import RotatingFileHandler


# TODO: complete
def configure_logging(app):
    # if app.debug or app.testing:
    #     return

    log_dir = os.path.join(app.root_path, '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'microblog.log'),
        maxBytes=10240,
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')
