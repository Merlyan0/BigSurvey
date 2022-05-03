import datetime

import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Attempt(SqlAlchemyBase, SerializerMixin):
    """
    Модель попыток пользователей.
    """
    __tablename__ = 'attempts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    answers = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    survey = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
