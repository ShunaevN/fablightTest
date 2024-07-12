import datetime
import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    """ describe ORM schemas of user in database"""
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    def __repr__(self):
        return f"{self.__class__.__name__} {self.id} {self.is_admin} {self.name} {self.email}"

    def set_password(self, password):
        """ set hashed password """
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        """ check input password with hashed password in database """
        return check_password_hash(self.hashed_password, password)