from datetime import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy_serializer import SerializerMixin

from panel.data.db_session import SqlAlchemyBase

association_table = sqlalchemy.Table('associate_users_to_conference', SqlAlchemyBase.metadata,
                                     sqlalchemy.Column('user', INTEGER(unsigned=True),
                                                       sqlalchemy.ForeignKey('all_users.user_id')),
                                     sqlalchemy.Column('conference', INTEGER(unsigned=True),
                                                       sqlalchemy.ForeignKey('all_conferences.conference_id'))
                                     )


class Conference(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'all_conferences'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True, autoincrement=True)
    conference_id = sqlalchemy.Column(INTEGER(unsigned=True), unique=True, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String(300))
    photo = sqlalchemy.Column(sqlalchemy.String(300))
    owner = sqlalchemy.Column(sqlalchemy.INTEGER)
    last_message = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    members = orm.relation("User",
                           secondary="associate_users_to_conference",
                           backref="all_conferences")
    msg_count = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)  # Все сообщения беседы - сумма сообщений участников

    custom_roles = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)
    pinned_message_id = sqlalchemy.Column(sqlalchemy.INTEGER, nullable=True)

    anti_obscene = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    auto_kick = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
