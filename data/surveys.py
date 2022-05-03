import datetime

import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash


class Survey(SqlAlchemyBase, SerializerMixin):
    """
    Модель опроса.
    """
    __tablename__ = 'surveys'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    ask_name = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    private = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    private_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    def set_password(self, password) -> None:
        """
        Задать пароль.
        """
        self.hashed_password = generate_password_hash(password)
