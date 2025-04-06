from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database.connection import SessionLocal, engine, Base
from .models.User import User
from .crud.user import *
from .crud.button import *
from .config import SWAGGER_HEADERS, swagger_ui_parameters
from .schemas.user import *
from .schemas.button import *


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

# FastAPI 기본 경로
@app.get("/")
def read_root():
    return {"Hello": "World"}

# 사용자 추가 API
@app.post("/add-user/", description="사용자 추가", tags=["User"])
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

# 모든 사용자 조회 API
@app.get("/get-users/", description="모든 사용자 조회", tags=["User"])
def read_users(db: Session = Depends(get_db)):
    return get_users(db)

# 버튼 로그 추가 API
@app.post("/add-button-log/", description="버튼 클릭 로그 추가", tags=["Button"])
def button_log_add(button_log: ButtonLogAdd, db: Session = Depends(get_db)):
    return add_button_log(db, button_log)

# 버튼 추천 API
@app.post("/recommend-button/", description="버튼 추천 (최근 1주일 가장 많은 순서대로 리턴)", tags=["Button"])
def button_recommend(recommend: ButtonRecommend, db: Session = Depends(get_db)):
    return recommend_buttons(db, recommend)
