from sqlalchemy.orm import Session
from app.models.Chat import Message
from app.models.User import User
from sqlalchemy import or_, and_

def get_messages(db: Session, user_id: str):
    user_id2 = db.query(User.nok_id).filter(User.user_id == user_id).scalar()
    return db.query(Message).filter(
        or_(
            and_(Message.user_id == user_id, Message.to_whom == user_id2),
            and_(Message.user_id == user_id2, Message.to_whom == user_id)
        )
    ).order_by(Message.created_at).all()

def save_message_to_db(db: Session, user_id: str, to_whom: str, content: str):
    new_message = Message(
        user_id=user_id,
        content=content,
        to_whom=to_whom
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message
