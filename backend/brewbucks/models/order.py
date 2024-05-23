from datetime import datetime, timezone
from . import db
from .payments import PaymentStatus
from enum import Enum


class OrderStatus(Enum):
    Processing = 1
    Making = 2
    Completed = 3
    Cancelled = 4


class Orders(db.Model):
    __tablename__ = "orders"

    order_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
        index=True,
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    order_status = db.Column(
        db.Enum(OrderStatus), nullable=False, default=OrderStatus.Processing
    )
    payment_status = db.Column(
        db.Enum(PaymentStatus), nullable=False, default=PaymentStatus.Pending
    )
    order_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
    total = db.Column(db.Float, nullable=False)
    rewards_added = db.Column(db.Integer, nullable=False, default=0)
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
            "order_id": self.order_id,
            "user_id": self.user_id,
            "order_status": self.order_status.name,
            "payment_status": self.payment_status.name,
            "order_date": self.order_date,
            "total": self.total,
            "rewards_added": self.rewards_added,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
