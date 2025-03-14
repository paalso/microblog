from flask import (
    flash,
    jsonify,
    redirect,
    render_template,
url_for
)
from flask_login import current_user, login_user

import sqlalchemy as sa
from app import db
from app.models import User
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'paalso'}
    return render_template(
        'index.html',
        user=user
    )

@app.route('/posts')
def posts_index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('posts_index.html', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


# TODO: remove after debugging
def _config_to_dict(config):
    return {key: str(value) for key, value in config.items()}


@app.route('/config')
def app_config():
    app.logger.info("Config: %s", app.config)
    config_dict = _config_to_dict(app.config)
    return jsonify(config_dict)
