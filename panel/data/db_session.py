import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_name='main_db'):
    global __factory

    if __factory:
        return

    if not db_name or not db_name.strip():
        raise Exception("Необходимо указать имя базы данных.")

    conn_str = f'mysql+mysqldb://root:godbotpassword@34.76.42.154:3306/{db_name.strip()}?charset=utf8'
    print(conn_str)

    engine = sa.create_engine(conn_str)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
