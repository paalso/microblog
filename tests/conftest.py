# tests/conftest.py
import pytest

from app import create_app, db


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",  # in-memory test db
        WTF_CSRF_ENABLED=False  # to simplify forms testing
    )
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test Flask client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Flask CLI runner."""
    return app.test_cli_runner()
