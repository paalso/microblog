import sqlalchemy as sa
import sqlalchemy.orm as so

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from app.config import Config
from app.logging import init_logging

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'main.login'

mail = Mail()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    init_logging(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    from app.routes import main_bp
    app.register_blueprint(main_bp, url_prefix='')

    from app.errors import errors_bp
    app.register_blueprint(errors_bp, url_prefix='')

    @app.shell_context_processor
    def make_shell_context():
        return {'sa': sa, 'so': so, 'db': db, 'session': db.session}

    return app
