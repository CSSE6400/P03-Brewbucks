from datetime import datetime, timezone
from . import db


class OrderItems(db.Model):
    __tablename__ = "order_items"

    order_item_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
        index=True,
    )
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), nullable=False)
    menu_item_id = db.Column(
        db.Integer, db.ForeignKey("menu_items.item_id"), nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)
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
            "order_item_id": self.order_item_id,
            "order_id": self.order_id,
            "menu_item_id": self.menu_item_id,
            "quantity": self.quantity,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
