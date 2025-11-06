from datetime import datetime, timezone

import sqlalchemy.orm as so


class TimestampMixin:
    created_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
