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

    def __repr__(self):
        return f'{self.conference.__repr__(False)}\n\n' \
               f'{self.user}\n' \
               f'role: {self.rights}\n' \
               f'messages: {self.msg_count}\n' \
               f'invited_by\n' \
               f'=====permissions======\n' \
               f'is_admin: {self.is_admin}\n' \
               f'is_owner: {self.is_owner}\n' \
               f'join_date: {self.join_date}\n' \
               f'is_muted: {self.is_muted}\n' \
               f'is_banned: {self.invited_by}\n' \
               f'is_leave: {self.is_leave}\n' \
               f'warns: {self.warns}\n' \
               f'kicks: {self.kick}\n' \
               f'rights: {self.rights}\n' \
               f'title_change: {self.title_change}\n' \
               f'photo_change: {self.photo_change}\n' \
               f'kick: {self.kick}\n' \
               f'warn: {self.warn}\n' \
               f'watch_stat: {self.watch_stat}\n' \
               f'kick_immunity: {self.kick_immunity}\n' \
               f'warn_immunity: {self.warn_immunity}\n'
