import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from panel.data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'all_users'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True, autoincrement=True)
    vk_id = sqlalchemy.Column(sqlalchemy.INTEGER)
    name = sqlalchemy.Column(sqlalchemy.String(120))
    surname = sqlalchemy.Column(sqlalchemy.String(120))
    conferences = sqlalchemy.Column(sqlalchemy.String(2000))  # Те, в которых состоит юзер
    msg_count = sqlalchemy.Column(sqlalchemy.INTEGER)  # Сообщения со всех бесед
    # (сделаем регулярное обновление по всем пользователям, чтобы не грузить БД (и чтобы можно было заморозить топ))
    warns = sqlalchemy.Column(sqlalchemy.INTEGER)
