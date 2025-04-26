from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class FCMToken(Base):
    __tablename__ = "fcm_tokens"
    __table_args__ = {"extend_existing": True}

    user_id = Column(String(32), primary_key=True)
    token = Column(String(256), nullable=False, index=True)