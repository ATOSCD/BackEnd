from app.models.Notification import Notifications
from sqlalchemy.orm import Session

def save_noti_to_db(db: Session, user_id: int, title: str, body: str):
    new_noti = Notifications(
        user_id=user_id,
        title=title,
        body=body
    )
    db.add(new_noti)
    db.commit()
    db.refresh(new_noti)
    return new_noti