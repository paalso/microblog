import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False))
    POSTS_PER_PAGE = os.environ.get('POSTS_PER_PAGE', 20)

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL')
        or 'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
    )
