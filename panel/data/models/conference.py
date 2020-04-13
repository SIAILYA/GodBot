import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from panel.data.db_session import SqlAlchemyBase


class Conference(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'all_conferences'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True, autoincrement=True)
    vk_id = sqlalchemy.Column(sqlalchemy.INTEGER)
    conf_name = sqlalchemy.Column(sqlalchemy.String(120), nullable=True)
    members = sqlalchemy.Column(sqlalchemy.String(5000))
    msg_count = sqlalchemy.Column(sqlalchemy.INTEGER)  # Все сообщения беседы - сумма сообщений
    # всех участников. Обновление раз в n минут
    # TODO: Добавить поля, сделать связь
