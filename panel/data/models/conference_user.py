import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy_serializer import SerializerMixin

from panel.data.db_session import SqlAlchemyBase


class ConferenceUser(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = f'main_table'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(INTEGER(unsigned=True),
                                sqlalchemy.ForeignKey('all_users.user_id'),
                                index=True)
    conference_id = sqlalchemy.Column(INTEGER(unsigned=True),
                                      sqlalchemy.ForeignKey('all_conferences.conference_id'),
                                      index=True)

    nickname = sqlalchemy.Column(sqlalchemy.String(20), nullable=True)
    msg_count = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)

    invited_by = sqlalchemy.Column(INTEGER(unsigned=True))
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_owner = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    join_date = sqlalchemy.Column(sqlalchemy.String(10), nullable=True)

    is_muted = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_banned = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_leave = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    warns = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    kicks = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)  # Сколько раз был кикнут
    rights = sqlalchemy.Column(sqlalchemy.String(50))  # Только название роли!

    title_change = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    photo_change = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    kick = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    warn = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    watch_stat = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    kick_immunity = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    warn_immunity = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    conference = orm.relation('Conference')
    user = orm.relation('User')
