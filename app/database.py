from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.models import Base

# SQLite-файл в корне проекта
SQLALCHEMY_DATABASE_URL = "sqlite:///./sportster.db"

# connect_args нужны для SQLite, чтобы работало в одном потоке
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Создаём таблицы, если их ещё нет.
    Вызываем один раз при старте приложения.
    """
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """
    Депенденси для FastAPI:
    при каждом запросе создаёт сессию и закрывает её после.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
