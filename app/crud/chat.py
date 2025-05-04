from sqlalchemy.orm import Session
from app.models.Chat import Message
from app.models.User import User
from sqlalchemy import or_

def get_messages(db: Session, user_id: int):
    return db.query(Message).filter(
        or_(Message.user_id == user_id, Message.user_id == db.query(User.nok_id).filter(User.user_id == user_id).scalar())
    ).order_by(Message.created_at).all()

def save_message_to_db(db: Session, user_id: int, content: str):
    new_message = Message(
        user_id=user_id,
        content=content
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message
