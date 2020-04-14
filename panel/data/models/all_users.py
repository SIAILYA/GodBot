import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from panel.data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'all_users'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.INTEGER)
    name = sqlalchemy.Column(sqlalchemy.String(120))
    surname = sqlalchemy.Column(sqlalchemy.String(120))
    sex = sqlalchemy.Column(sqlalchemy.INTEGER, nullable=True)
    conferences = sqlalchemy.Column(sqlalchemy.String(5000))  # Те, в которых состоит юзер
    msg_count = sqlalchemy.Column(sqlalchemy.INTEGER)  # Сообщения со всех бесед
    is_closed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    # (сделаем регулярное обновление по всем пользователям, чтобы не грузить БД)
