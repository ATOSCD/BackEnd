from sqlalchemy.orm import Session
from app.models.Chat import Message
from app.models.User import User
from sqlalchemy import or_

def get_messages(db: Session, user_id: int):
    return db.query(Message).filter(
        or_(Message.user_id == user_id, Message.user_id == db.query(User.nok_id).filter(User.user_id == user_id).scalar())
    ).order_by(Message.created_at).all()
