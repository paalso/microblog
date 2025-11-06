import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db
from app.models.mixins import TimestampMixin


class Post(TimestampMixin, db.Model):
    __tablename__ = 'posts'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(256))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'),
                                               index=True)

    author: so.Mapped['User'] = so.relationship(    # noqa: F821
        'User', back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)
