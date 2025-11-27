from datetime import datetime, timezone
from urllib.parse import urlsplit

import sqlalchemy as sa
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from app.forms import EditProfileForm, LoginForm, RegistrationForm
from app.models.user import User

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/index')
@login_required
def index():
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
    return render_template('index.html', title='Home', posts=posts)


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    main_bp.logger.debug(f'current_user: ${current_user}')
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        main_bp.logger.debug(f'user: ${user}')

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))

        login_user(user, remember=form.remember_me.data)

        main_bp.logger.debug(f'request.args: ${request.args}')
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@main_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        main_bp.logger.debug(f'user to register: ${user}')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@main_bp.route('/users')
def users():
    if current_user.is_anonymous or not current_user.is_admin:
        flash(
            "You don't have the necessary permissions to view the user list.")
        return redirect(url_for('main.index'))

    users = db.session.query(User).all()
    return render_template('admin/users.html', title='Users', users=users)


@main_bp.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@main_bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@main_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


# ------------------------------------------------------------
@main_bp.route('/debug')
def debug():
    print("--- Request context info ---")
    print("request:", request)
    print("path:", request.path)
    print("method:", request.method)
    print("session:", dict(session))
    print("current_user:", current_user)
    print("g:", g)
    return "Check your terminal or log!"
