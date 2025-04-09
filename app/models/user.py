from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    user_id = Column(String(32), primary_key=True)
    name = Column(String(32), nullable=False, index=True)
    password = Column(String(32), nullable=False)
    nok_id = Column(String(32), default=None)
