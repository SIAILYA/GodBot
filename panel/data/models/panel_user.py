import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from panel.data.db_session import SqlAlchemyBase


class PanelUser(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'panel_users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String(30), nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String(30))
    access_rights = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    password_hash = sqlalchemy.Column(sqlalchemy.String(120), nullable=True)

    def __repr__(self):
        return f"PanelUser #{self.id} {self.login} {self.access_rights}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


if __name__ == '__main__':
    print(generate_password_hash('123qw'))
