from sqlalchemy.orm import Session
from app.models.User import User
from app.schemas.user import *
from werkzeug.security import check_password_hash, generate_password_hash

def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.user_id == user_id).first()

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
    if user.nok_id != None:
        user_nok = db.query(User).filter(User.user_id == user.nok_id).first()
        user_nok.nok_id = None
        db.commit()
        db.refresh(user_nok)
        
    if user2.nok_id != None:
        user2_nok = db.query(User).filter(User.user_id == user2.nok_id).first()
        user2_nok.nok_id = None
        db.commit()
        db.refresh(user2_nok)

    if user and user2:
        user.nok_id = dto.nok_id
        user2.nok_id = dto.user_id
        db.commit()
        db.refresh(user)
        db.refresh(user2)
        return {"nok_name": user2.name}
    else:
        return {"nok_name": None}
    
def get_nok_id(db: Session, dto: GetNok):
    user = db.query(User).filter(User.user_id == dto.user_id).first()
    
    if user and user.nok_id:
        nok_user = db.query(User).filter(User.user_id == user.nok_id).first()
        return {"nok_id": nok_user.user_id, "nok_name": nok_user.name}
    else:
        return {"nok_id": None, "nok_name": None}
    
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

def user_login(db: Session, data: Userlogin):
    user = db.query(User).filter(User.user_id == data.user_id).first()
    
    if not user:
        return 0
    if not check_password_hash(user.password, data.password):
        return 0
    if user.patient == 1:
        return 1
    elif user.patient == 2:
        return 2
    else:
        return 0

def id_check(db: Session, data: IdCheck):
    user = db.query(User).filter(User.user_id == data.user_id).first()
    
    if not user:
        return 1
    else:
        return 0
    
