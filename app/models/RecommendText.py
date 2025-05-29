from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, func, Boolean
from sqlalchemy.orm import relationship
from app.database.connection import Base

class RecommendChat(Base):
    __tablename__ = "recommend_chats"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    recommend_text = Column(Text, nullable=False)

class RecommendChatForUser(Base):
    __tablename__ = "recommend_chats_for_user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(32), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    recommend_chat = Column(Text, nullable=False)
    count = Column(Integer, default=0)