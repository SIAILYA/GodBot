import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy_serializer import SerializerMixin

from panel.data.db_session import SqlAlchemyBase

association_table = sqlalchemy.Table('associate_conferences_to_user', SqlAlchemyBase.metadata,
                                     sqlalchemy.Column('conference', INTEGER(unsigned=True),
                                                       sqlalchemy.ForeignKey('all_conferences.conference_id')),
                                     sqlalchemy.Column('user', INTEGER(unsigned=True),
                                                       sqlalchemy.ForeignKey('all_users.user_id'))
                                     )


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'all_users'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(INTEGER(unsigned=True), unique=True, nullable=True)

    name = sqlalchemy.Column(sqlalchemy.String(120))
    surname = sqlalchemy.Column(sqlalchemy.String(120))

    is_closed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    sex = sqlalchemy.Column(sqlalchemy.INTEGER, nullable=True)

    conferences = orm.relation("Conference",
                               secondary="associate_conferences_to_user",
                               backref="all_users")  # Те, в которых состоит юзер

    msg_count = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)  # Сообщения со всех бесед
    # (сделаем регулярное обновление по всем пользователям, чтобы не грузить БД)
