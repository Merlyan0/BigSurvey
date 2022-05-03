import sqlalchemy as sa                   # БД
import sqlalchemy.orm as orm              # Подключаем функционал ORM
from sqlalchemy.orm import Session        # Объект Session отвечает за соединение с БД
import sqlalchemy.ext.declarative as dec  # Поможет объявить БД


SqlAlchemyBase = dec.declarative_base()  # БД

__factory = None                         # нужна для получения сессий подключения к БД


def global_init(db_file) -> None:
    """
    Принимает на вход адрес базы данных, затем проверяет, не создали ли мы уже фабрику подключений
    (то есть не вызываем ли мы функцию не первый раз). Если уже создали, то завершаем работу,
    так как начальную инициализацию надо проводить только единожды.

    :param db_file: Адрес БД
    :return: None
    """
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models  # в этом месте SQL узнаёт о всех моделях

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    """
    Нужна для получения сессии подключения к нашей базе данных

    :return: Session
    """
    global __factory
    return __factory()
