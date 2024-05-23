from datetime import datetime, timezone
from . import db


class Rewards(db.Model):
    __tablename__ = "rewards"

    # customer id from customer table
    customer_id = db.Column(
        db.Integer, db.ForeignKey("users.user_id"), primary_key=True, nullable=False
    )
    total_points = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "total_points": self.total_points,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
