from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

DB_URL = "mysql+pymysql://root:123456@localhost:3306/training_db"
engine = create_engine(DB_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()