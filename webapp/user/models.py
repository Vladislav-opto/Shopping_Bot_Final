from flask_login import UserMixin
from sqlalchemy import ForeignKey

from webapp.webapp.model import db

class AuthWebApp(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), index=True, nullable=True)
    last_name = db.Column(db.String(50), index=True, nullable=True)
    email = db.Column(db.String(100), unique=True)

    def __repr__(self) -> str:
        return '<User {}>'.format(self.first_name)


class CategoryByUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(AuthWebApp.id), nullable=True)
    category_id = db.Column(db.Integer, nullable=True)
    receipt_id = db.Column(db.Integer, nullable=True)
    upload = db.Column(db.DateTime, nullable=True)

    def __repr__(self) -> str:
        return '<ID {}>'.format(self.id)


class AuthCodeByUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(AuthWebApp.id), nullable=True)
    auth_code = db.Column(db.Integer, nullable=True)
    upload = db.Column(db.DateTime, nullable=True)

    def __repr__(self) -> str:
        return f'{self.auth_code}'
