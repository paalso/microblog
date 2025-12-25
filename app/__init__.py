import sqlalchemy as sa
import sqlalchemy.orm as so

from flask import current_app, request, Flask
from flask_babel import Babel, lazy_gettext as _l
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
login.login_message = _l('Please log in to access this page.')

mail = Mail()
moment = Moment()


def get_locale():
    lang = request.cookies.get('lang')
    if lang in current_app.config['LANGUAGES']:
        current_app.logger.debug(f'ℹ️ Language (from cookie): {lang})')
        return lang

    lang_best_match = request.accept_languages.best_match(
        current_app.config['LANGUAGES']
    )

    current_app.logger.debug(
        f'ℹ️ request.accept_languages: {request.accept_languages})')
    current_app.logger.debug(
        f'ℹ️ Language (best_match): {lang_best_match})')
    return lang_best_match


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    init_logging(app)
    babel = Babel(app, locale_selector=get_locale)  # noqa: F841

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
