from datetime import datetime, timezone
from . import db
from enum import Enum


class Roles(Enum):
    Customer = "customer"
    Employee = "employee"


class Users(db.Model):
    __tablename__ = "users"

    user_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
        index=True,
    )
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    role = db.Column(db.Enum(Roles), nullable=False, default=Roles.Customer)
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
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "role": self.role.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
