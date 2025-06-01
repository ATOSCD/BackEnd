from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, func, Boolean
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(32), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    is_read = Column(Boolean, default=False)
    to_whom = Column(String(32), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=True)


