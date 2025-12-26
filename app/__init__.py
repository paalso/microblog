import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import Flask
from flask_babel import lazy_gettext as _l

from app.config import Config
from app.logging import init_logging
from app.extensions import (
    db, migrate, login, mail, moment, babel
)
from app.i18n import get_locale


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_logging(app)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    # Flask-Login config
    login.login_view = 'main.login'
    login.login_message = _l('Please log in to access this page.')

    # Blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    from app.errors import errors_bp
    app.register_blueprint(errors_bp)

    # Shell
    @app.shell_context_processor
    def make_shell_context():
        return {'sa': sa, 'so': so, 'db': db, 'session': db.session}

    return app
