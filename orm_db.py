from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models_orm import Base
import config

# Формируем строку подключения из config.py
DB_URL = f"mysql+mysqlconnector://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}?charset=utf8mb4"

engine = create_engine(DB_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

# Для Alembic или ручного создания таблиц
# Base.metadata.create_all(engine) 