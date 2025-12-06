from datetime import datetime, timezone
from urllib.parse import urlsplit

import sqlalchemy as sa
from flask import (
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user

from app import Config, db
from app.forms import (
    EditProfileForm,
    EmptyForm,
    LoginForm,
    PostForm,
    RegistrationForm,
    ResetPasswordForm,
    ResetPasswordRequestForm,
)
from app.models import Post, User
from app.utils.email import send_email, send_password_reset_email

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        current_app.logger.info(
            f'📝 New post created by {current_user.username}: '
            f'"{post.body[:30]}..."')
        flash('Your post is now live!')
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    posts = db.paginate(current_user.following_posts(), page=page,
                        per_page=Config.POSTS_PER_PAGE, error_out=False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template(
        'pages/index.html', title='Home', form=form,
        posts=posts.items, next_url=next_url, prev_url=prev_url
    )


@main_bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.created_at.desc())
    posts = db.paginate(query, page=page,
                        per_page=Config.POSTS_PER_PAGE, error_out=False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template(
        'pages/index.html', title='Explore', posts=posts.items,
        next_url=next_url, prev_url=prev_url
    )


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))

        if user is None:
            current_app.logger.warning(
                f'❌ Login failed — unknown username "{form.username.data}"')
            flash('Invalid username or password')
            return redirect(url_for('main.login'))

        if not user.check_password(form.password.data):
            current_app.logger.warning(
                f'🔐 Wrong password attempt for user "{form.username.data}"')
            flash('Invalid username or password')
            return redirect(url_for('main.login'))

        login_user(user, remember=form.remember_me.data)
        current_app.logger.info(f'🔑 Logged in: {user.username}')

        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('pages/login.html', title='Sign In', form=form)


@main_bp.route('/logout')
def logout():
    username = current_user.username
    logout_user()
    current_app.logger.info(f'🚪 User logged out: {username}')
    return redirect(url_for('main.index'))


@main_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        current_app.logger.debug(f'⚠️ User {current_user.username} '
                                f'is already authenticated. No need to log in.')
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('main.login'))
    return render_template('pages/reset_password_request.html',
                           title='Reset Password', form=form)


@main_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('main.login'))
    return render_template('email/reset_password.html', form=form)


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        current_app.logger.info(
            f'👤 Already authenticated user tried to access /register: '
            f'{current_user}'
        )
        return redirect(url_for('main.index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        current_app.logger.info(
            f'📝 Registration attempt: '
            f'username={form.username.data}, email={form.email.data}'
        )

        user = User(username=form.username.data, email=form.email.data)
        current_app.logger.debug(f'🧱 User object created: {user}')

        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        current_app.logger.info(
            f'🎉 New user registered successfully: {user.username}'
        )

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))

    return render_template('pages/register.html', title='Register', form=form)


@main_bp.route('/user/<username>')
@login_required
def user(username):
    current_app.logger.debug(
        f'👤 Current user accessing profile: {current_user}'
    )
    current_app.logger.info(
        f'🔎 Profile request for username="{username}"'
    )

    user = db.first_or_404(sa.select(User).where(User.username == username))

    page = request.args.get('page', 1, type=int)

    query = (
        sa.select(Post)
        .where(Post.user_id == user.id)
        .order_by(Post.created_at.desc())
    )

    posts = db.paginate(
        query, page=page, per_page=Config.POSTS_PER_PAGE, error_out=False
    )

    next_url = (
        url_for('user', username=user.username, page=posts.next_num)
        if posts.has_next else None
    )
    prev_url = (
        url_for('user', username=user.username, page=posts.prev_num)
        if posts.has_prev else None
    )

    form = EmptyForm()
    return render_template('pages/user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@main_bp.before_request
def before_request():
    if current_user.is_authenticated:
        # current_app.logger.debug(
        #     f'⏱️ Updating last_seen for {current_user}'
        # )
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@main_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    current_app.logger.debug(
        f'👤 Edit profile request by: {current_user}'
    )

    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_app.logger.info(
            f'📝 Profile update submitted: username={form.username.data}'
        )

        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        current_app.logger.info(
            f'✅ Profile updated successfully for user={current_user.username}'
        )

        flash('Your changes have been saved.')
        return redirect(url_for('main.user', username=current_user.username))

    elif request.method == 'GET':
        current_app.logger.debug(
            f'📄 Pre-filling edit form for user={current_user.username}'
        )
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template(
        'pages/edit_profile.html', title='Edit Profile', form=form
    )


@main_bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    current_app.logger.debug(
        f'👥 Follow attempt: '
        f'current_user={current_user.username}, target={username}'
    )

    form = EmptyForm()

    if not form.validate_on_submit():
        current_app.logger.warning('⚠️ Invalid follow form submission')
        return redirect(url_for('main.index'))

    user = db.first_or_404(sa.select(User).where(User.username == username))
    current_app.logger.debug(f'🔎 Follow target resolved: {user}')

    if user == current_user:
        current_app.logger.warning('⚠️ User tried to follow themselves')
        flash('You cannot follow yourself!')

    elif current_user.is_following(user):
        current_app.logger.info(
            f'ℹ️ Already following: {current_user.username} → {username}'
        )
        flash(f'You are already following {username}.')

    else:
        current_user.follow(user)
        db.session.commit()
        current_app.logger.info(
            f'➕ New follow: {current_user.username} → {username}'
        )
        flash(f'You are now following {username}!')

    return redirect(url_for('main.user', username=username))


@main_bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    current_app.logger.debug(
        f'👥 Unfollow attempt: '
        f'current_user={current_user.username}, target={username}'
    )

    form = EmptyForm()

    if not form.validate_on_submit():
        current_app.logger.warning('⚠️ Invalid unfollow form submission')
        return redirect(url_for('main.index'))

    user = db.first_or_404(sa.select(User).where(User.username == username))
    current_app.logger.debug(f'🔎 Unfollow target resolved: {user}')

    if user == current_user:
        current_app.logger.warning('⚠️ User tried to unfollow themselves')
        flash('You cannot unfollow yourself!')

    elif not current_user.is_following(user):
        current_app.logger.info(
            f'ℹ️ Attempt to unfollow non-followed user: {username}'
        )
        flash(f'You are not following {username}.')

    else:
        current_user.unfollow(user)
        db.session.commit()
        current_app.logger.info(
            f'➖ Unfollow: {current_user.username} → {username}'
        )
        flash(f'You have unfollowed {username}!')

    return redirect(url_for('main.user', username=username))


# ---- For admin / debug only ----------------------------------------
@main_bp.route('/users')
@login_required
def users():
    if not current_user.is_admin:
        flash("You don't have the permissions to view the user list.")
        return redirect(url_for('main.index'))

    sort = request.args.get('sort', 'id')

    # TODO: add desc / reversed sort order
    sort_map = {
        'id': User.id,
        'username': User.username,
        'created_at': User.created_at
    }

    sort_column = sort_map.get(sort, User.id)

    stmt = sa.select(User).order_by(sort_column)
    users = db.session.scalars(stmt).all()

    return render_template('admin/users.html', users=users, sort=sort)


@main_bp.route('/posts')
def posts():
    current_app.logger.debug(f'current_user: ${current_user}')
    if current_user.is_anonymous or not current_user.is_admin:
        flash(
            "You don't have the permissions to view the posts list.")
        return redirect(url_for('main.index'))

    posts = db.session.query(Post).all()
    return render_template('admin/posts.html', title='Posts', posts=posts)


# ------------------------------------------------------------
@main_bp.route('/debug')
def debug():
    print('--- Request context info ---')
    print('request:', request)
    print('path:', request.path)
    print('method:', request.method)
    print('session:', dict(session))
    print('current_user:', current_user)
    print('g:', g)
    return 'Check your terminal or log!'


@main_bp.route('/hello')
def hello():
    name = request.args.get('name', 'Paul')
    return f'<h1>Hello, {name}!</h1>'


@main_bp.route('/test_send_email')
def test_send_email():
    message = request.args.get('message')
    if not message:
        return 'No message: nothing to email'

    message_prefix = message if len(message) < 10 else f'{message[:7]}...'
    subject = f'Test email from Microblog: {message_prefix}'
    sender = Config.ADMINS[0]
    recipients = [sender]
    text_body = message
    send_email(subject, sender, recipients, text_body)

    return 'Sending email. See logs for details...'
