from sqlalchemy.orm import Session
from app.models.User import User
from app.schemas.user import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(
        user_id=user.user_id, 
        name=user.name, 
        password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()
