import os

basedir = os.path.abspath(os.path.dirname(__file__))
# e.g.
# __file__: /home/paalso/Courses/microblog/app/config.py
# os.path.dirname(__file__): /home/paalso/Courses/microblog/app
# basedir: /home/paalso/Courses/microblog/app


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or
                               'sqlite:///' + os.path.join(basedir, 'app.db'))
