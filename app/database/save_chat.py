from app.models.Chat import Message
from sqlalchemy.orm import Session

def save_message_to_db(db: Session, user_id: int, content: str):
    new_message = Message(
        user_id=user_id,
        content=content
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message