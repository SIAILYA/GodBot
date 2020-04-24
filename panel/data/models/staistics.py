from datetime import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy_serializer import SerializerMixin

from panel.data.db_session import SqlAlchemyBase


class Statistics(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = f'statistics'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.now().date)
    member_id = sqlalchemy.Column(INTEGER(unsigned=True),
                                  sqlalchemy.ForeignKey('all_users.user_id'),
                                  index=True)
    conference_id = sqlalchemy.Column(INTEGER(unsigned=True),
                                      sqlalchemy.ForeignKey('all_conferences.conference_id'),
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

    def inc(self, hr):
        if hr == 0:
            self.h0 += 1
        elif hr == 1:
            self.h1 += 1
        elif hr == 2:
            self.h2 += 1
        elif hr == 3:
            self.h3 += 1
        elif hr == 4:
            self.h4 += 1
        elif hr == 5:
            self.h5 += 1
        elif hr == 6:
            self.h6 += 1
        elif hr == 7:
            self.h7 += 1
        elif hr == 8:
            self.h8 += 1
        elif hr == 9:
            self.h9 += 1
        elif hr == 10:
            self.h10 += 1
        elif hr == 11:
            self.h11 += 1
        elif hr == 12:
            self.h12 += 1
        elif hr == 13:
            self.h13 += 1
        elif hr == 14:
            self.h14 += 1
        elif hr == 15:
            self.h15 += 1
        elif hr == 16:
            self.h16 += 1
        elif hr == 17:
            self.h17 += 1
        elif hr == 18:
            self.h18 += 1
        elif hr == 19:
            self.h19 += 1
        elif hr == 20:
            self.h20 += 1
        elif hr == 21:
            self.h21 += 1
        elif hr == 22:
            self.h22 += 1
        elif hr == 23:
            self.h23 += 1

    def sum(self):
        return sum([self.h0, self.h1, self.h2, self.h3, self.h4, self.h5, self.h6, self.h7, self.h8, self.h9, self.h10,
                    self.h11, self.h12, self.h13, self.h14, self.h15, self.h16, self.h17, self.h18, self.h19, self.h20,
                    self.h21, self.h22, self.h23])
