from sqlalchemy.orm import Session
from app.models.user import User

def create_user(db: Session, name: str, password: str):
    db_user = User(name=name, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()
