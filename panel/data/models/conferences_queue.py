import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from panel.data.db_session import SqlAlchemyBase


class ConferencesQueue(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'queue'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True, autoincrement=True)
    conference_id = sqlalchemy.Column(sqlalchemy.INTEGER)
    before_notification = sqlalchemy.Column(sqlalchemy.INTEGER, default=10)
