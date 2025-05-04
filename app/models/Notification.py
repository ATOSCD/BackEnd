from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, func, Boolean
from app.database.connection import Base

class Notifications(Base):
    __tablename__ = "notifications"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(32), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(String(100), nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())