from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///./app.db",
                       connect_args={"check_same_thread" : False})
SessionLocal = sessionmaker(bind = engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    with SessionLocal() as db:
        yield db