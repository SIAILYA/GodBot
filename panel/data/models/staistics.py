from datetime import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from panel.data.db_session import SqlAlchemyBase


class Statistics(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = f'statistics'

    date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.now)
    member_id = sqlalchemy.Column(sqlalchemy.INTEGER, sqlalchemy.ForeignKey('all_users.user_id'),
                                  index=True)
    conference_id = sqlalchemy.Column(sqlalchemy.INTEGER, sqlalchemy.ForeignKey('all_conferences.conference_id'),
                                      index=True)

    h0 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h1 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h2 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h3 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h4 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h5 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h6 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h7 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h8 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h9 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h10 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h11 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h12 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h13 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h14 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h15 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h16 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h17 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h18 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h19 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h20 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h21 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h22 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    h23 = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)

    conference = orm.relation('Conference')
    user = orm.relation('User')
