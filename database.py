from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./lifelens.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class LifeData(Base):
    __tablename__ = "lifedata"

    id = Column(Integer, primary_key=True, index=True)
    study = Column(Integer)
    sleep = Column(Integer)
    screen = Column(Integer)
    workout = Column(String)
    morning = Column(String)

Base.metadata.create_all(bind=engine)
