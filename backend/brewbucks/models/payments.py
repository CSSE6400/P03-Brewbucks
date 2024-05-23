from datetime import datetime, timezone
from . import db
from enum import Enum


class PaymentStatus(Enum):
    Pending = 1
    Paid = 2
    Refunded = 3


class Payments(db.Model):
    __tablename__ = "payments"

    payment_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
        index=True,
    )
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), nullable=False)
    payment_method = db.Column(db.Text, nullable=False, default="Demo Checkout")
    payment_status = db.Column(
        db.Enum(PaymentStatus), nullable=False, default=PaymentStatus.Pending
    )
    payment_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
    amount = db.Column(db.Float, nullable=False)
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
            "payment_id": self.payment_id,
            "order_id": self.order_id,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status.name,
            "payment_date": self.payment_date,
            "amount": self.amount,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
