from sqlalchemy.orm import Session
from app.models.User import User
from app.schemas.user import *
from werkzeug.security import check_password_hash, generate_password_hash

def create_user(db: Session, user: UserCreate):
    db_user = User(
        user_id=user.user_id, 
        name=user.name, 
        password=generate_password_hash(user.password),
        patient=user.patient
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
    
def find_patient(db: Session, data: FindUser):
    user = db.query(User).filter(User.user_id == data.user_id, User.patient == 2).first()
    
    if not user:
        return None
    if not check_password_hash(user.password, data.password):
        return None
    
    return_user = ReturnUser(
        user_id=user.user_id,
        name=user.name,
        nok_id=user.nok_id,
        patient=user.patient
    )
    
    return return_user
    
