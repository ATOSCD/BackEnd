from sqlalchemy import Column, Integer, String, DateTime, PrimaryKeyConstraint
from sqlalchemy.sql import func
from app.database.connection import Base
from datetime import datetime

class ButtonLog(Base):
    __tablename__ = "button_log"

    user_id = Column(String(32), nullable=False)
    button_id = Column(Integer, nullable=False)
    category = Column(String(32), nullable=False)
    date = Column(DateTime, nullable=False, default=func.now())

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'button_id', 'date'),
    )

class ButtonList(Base):
    __tablename__ = "button_list"

    user_id = Column(String(32), nullable=False)
    button_id = Column(Integer, nullable=False)
    category = Column(String(32), nullable=False)
    button_text = Column(String(50), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('user_id','category','button_id'),
    )
