import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from panel.data.db_session import SqlAlchemyBase


class PanelUser(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'panel_users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String(30), nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String(20), nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    def __repr__(self):
        return f"PanelUser #{self.id} {self.login}"


if __name__ == '__main__':
    print(generate_password_hash('123qw'))
