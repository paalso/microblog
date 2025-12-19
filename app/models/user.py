from datetime import datetime, timezone
from hashlib import md5
from time import time
from typing import Optional

import jwt
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login
from app.models.mixins import TimestampMixin

followers = sa.Table(
    'followers',
    db.metadata,
    # follower_id ----> User.id (who follows)
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('users.id'),
              primary_key=True),
    # followed_id ----> User.id (who is followed)
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('users.id'),
              primary_key=True)
)


class User(TimestampMixin, UserMixin, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.Mapped[list['Post']] = so.relationship(  # noqa: F821
        'Post', back_populates='author', lazy='dynamic')

    role: so.Mapped[str] = so.mapped_column(sa.String(20), default='user')

    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))

    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        sa.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # User.following = users I follow
    following: so.Mapped[set['User']] = so.relationship(
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        collection_class=set,
        back_populates='followers'
    )

    # User.followers = users who follow ME
    followers: so.Mapped[set['User']] = so.relationship(
        secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        collection_class=set,
        back_populates='following'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    @property
    def is_admin(self):
        return self.role == 'admin'

    def follow(self, user):
        self.following.add(user)

    def unfollow(self, user):
        self.following.discard(user)

    def is_following(self, user) -> bool:
        return user in self.following

    def followers_count(self) -> int:
        stmt = (
            sa.select(sa.func.count())
            .select_from(followers)
            .where(followers.c.followed_id == self.id)
        )
        return db.session.scalar(stmt)

    def following_count(self) -> int:
        stmt = (
            sa.select(sa.func.count())
            .select_from(followers)
            .where(followers.c.follower_id == self.id)
        )
        return db.session.scalar(stmt)

    def following_posts(self):
        Post = sa.orm.class_mapper(User).registry._class_registry['Post']

        following_ids = (
            sa.select(followers.c.followed_id)
            .where(followers.c.follower_id == self.id)
        )

        query = (
            sa.select(Post)
            .where(
                sa.or_(
                    Post.user_id.in_(following_ids),
                    Post.user_id == self.id,
                )
            )
            .order_by(Post.created_at.desc())
        )

        return query

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({
            'reset_password': self.id,
             'exp': time() + expires_in
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )['reset_password']
            current_app.logger.debug('🔐👤 User succesfully identified')
        except Exception:
            current_app.logger.debug(
                '⚠️ Token invalid or expired. User not fount')
            return
        return db.session.get(User, id)

    # TODO:
    # mutual_friends() — mutual followers
    # suggested_follows() — subscription recommendations

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
