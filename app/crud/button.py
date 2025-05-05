from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.User import User
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from app.models.Button import *
from app.schemas.button import *

def add_button_log(db: Session, button_log: ButtonLogAdd):
    log = ButtonLog(
        user_id=button_log.user_id,
        button_id=button_log.button_id,
        date=func.now()
    )
    db.add(log)
    db.commit()
    return button_log


def recommend_buttons(db: Session, recommend: ButtonRecommend):
    week = datetime.now() - timedelta(days=7)

    # 쿼리 작성: 최근 1주일간의 button_id를 개수로 정렬
    result = (
        db.query(ButtonLog.button_id, func.count(ButtonLog.button_id).label("count"))
        .filter(ButtonLog.date >= week)                  # 최근 1주일 데이터 필터링
        .filter(ButtonLog.user_id == recommend.user_id)  # 특정 사용자 필터링
        .group_by(ButtonLog.button_id)                   # button_id로 그룹화
        .order_by(desc("count"))                         # 개수로 내림차순 정렬
        .all()
    )

    return [row.button_id for row in result]

def custom_button(db: Session, data: CustomButton):
    button = ButtonList(
        user_id=data.user_id,
        button_id=data.button_id,
        category=data.category,
        button_text=data.button_text
    )
    m_button = db.merge(button)
    db.commit()
    db.refresh(m_button)
    return button

def get_button_by_category(db: Session, data: GetButtonByCategory):
    buttons = (
        db.query(ButtonList)
        .filter(ButtonList.user_id == data.user_id)
        .filter(ButtonList.category == data.category)
        .order_by(ButtonList.button_id)
        .all()
    )
    return buttons