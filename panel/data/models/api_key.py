import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from panel.data.db_session import SqlAlchemyBase


class ApiKey(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'panel_users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    key = sqlalchemy.Column(sqlalchemy.String(120), nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
