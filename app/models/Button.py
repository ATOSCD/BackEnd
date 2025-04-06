from sqlalchemy import Column, Integer, String, DateTime, PrimaryKeyConstraint
from sqlalchemy.sql import func
from app.database.connection import Base
from datetime import datetime

class ButtonLog(Base):
    __tablename__ = "button_log"

    user_id = Column(String(32), nullable=False)
    button_id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False, default=func.now())

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'button_id', 'date'),
    )
