import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase, SerializerMixin):
    """
    Модель всех вопросов.
    """
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    right = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    var = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    survey = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
