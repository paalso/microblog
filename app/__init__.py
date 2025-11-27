from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.logging_config import configure_logging

from app.config import Config

db = SQLAlchemy()           # почему не передаем сюда app
migrate = Migrate()         # почему не передаем сюда app
login = LoginManager()      # почему не передаем сюда app
login.login_view = 'login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    configure_logging(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.routes import main_bp
    app.register_blueprint(main_bp, url_prefix='')

    from app.errors import errors_bp
    app.register_blueprint(errors_bp, url_prefix='')

    return app
