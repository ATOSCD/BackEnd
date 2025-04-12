from sqlalchemy.orm import Session
from app.models.User import User
from app.schemas.user import UserCreate, SetNok

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

def set_nok_id(db: Session, dto: SetNok):
    user = db.query(User).filter(User.user_id == dto.user_id).first()
    user2 = db.query(User).filter(User.user_id == dto.nok_id).first()
    if user and user2:
        user.nok_id = dto.nok_id
        user2.nok_id = dto.user_id
        db.commit()
        db.refresh(user)
        db.refresh(user2)
        return {"message": "NOK ID 설정 완료", "user": user.name}
    else:
        return {"message": "사용자를 찾을 수 없습니다."}
