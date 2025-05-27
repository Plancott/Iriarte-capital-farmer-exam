from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Conexión a la base de datos SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()