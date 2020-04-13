import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from panel.data.db_session import SqlAlchemyBase


class ConferenceUser(SqlAlchemyBase, UserMixin, SerializerMixin):
    def __init__(self, conference_id):
        __tablename__ = f'conference_{conference_id}'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True, autoincrement=True)
    vk_id = sqlalchemy.Column(sqlalchemy.INTEGER)
    name = sqlalchemy.Column(sqlalchemy.String(120))
    surname = sqlalchemy.Column(sqlalchemy.String(120))
    # rights = TODO: Придумать как "шифровать" права пользователя (модель прав, строка из 0 и 1 и т.д.)
    msg_count = sqlalchemy.Column(sqlalchemy.INTEGER)
    msg_today = sqlalchemy.Column(sqlalchemy.INTEGER)
    warns = sqlalchemy.Column(sqlalchemy.INTEGER)
