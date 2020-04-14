import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from panel.data.db_session import SqlAlchemyBase


class Conference(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'all_conferences'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True, autoincrement=True)
    conference_id = sqlalchemy.Column(sqlalchemy.INTEGER)
    title = sqlalchemy.Column(sqlalchemy.String(300))
    photo = sqlalchemy.Column(sqlalchemy.String(300))
    members = sqlalchemy.Column(sqlalchemy.String(5000), default='')
    msg_count = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)  # Все сообщения беседы - сумма сообщений участников
    custom_roles = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)
    pinned_message = sqlalchemy.Column(sqlalchemy.String(5000), nullable=True)

    # TODO: Прочие параметры (например, антимат, автокик)
