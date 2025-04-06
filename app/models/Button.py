from sqlalchemy import Column, Integer, String, DateTime, PrimaryKeyConstraint
from app.database.connection import Base
from datetime import datetime

class ButtonLog(Base):
    __tablename__ = "botton_log"

    user_id = Column(String, nullable=False)
    button_id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'button_id', 'date'),
    )
