from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database.connection import SessionLocal, engine, Base
from .models.User import User
from .crud.user import create_user, get_users
from .config import SWAGGER_HEADERS, swagger_ui_parameters



# DB 테이블 생성 (최초 실행 시 필요)
Base.metadata.create_all(bind=engine)

app = FastAPI(swagger_ui_parameters=swagger_ui_parameters, **SWAGGER_HEADERS)

# 의존성 주입: DB 세션 가져오기
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 사용자 추가 API
@app.post("/users/")
def add_user(name: str, password: str, db: Session = Depends(get_db)):
    return create_user(db, name, password)

# 모든 사용자 조회 API
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return get_users(db)
