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
        category=button_log.category,
        date=func.now()
    )
    db.add(log)
    db.commit()
    return button_log

def recommend_buttons(db: Session, recommend: ButtonRecommend):
    week = datetime.now() - timedelta(days=7)

    buttons = (
        db.query(ButtonLog.user_id, ButtonLog.category, ButtonLog.button_id, func.count(ButtonLog.button_id).label("count"))
        .filter(ButtonLog.date >= week)
        .filter(ButtonLog.user_id == recommend.user_id)
        .group_by(ButtonLog.category, ButtonLog.button_id)
        .order_by(desc("count"))
        .all()
    )

    result = []
    for i in range(min(5,len(buttons))):
        button = buttons[i]
        button_info = (
            db.query(ButtonList)
            .filter(ButtonList.user_id == recommend.user_id)
            .filter(ButtonList.category == button.category)
            .filter(ButtonList.button_id == button.button_id)
            .first()
        )
        if button_info:
            result.append({
                "button_id": button_info.button_id,
                "category": button_info.category,
                "button_text": button_info.button_text,
                "count": button.count
            })

    return result

def recommend_buttons_by_category(db: Session, recommend: ButtonRecommendByCategory):
    week = datetime.now() - timedelta(days=7)

    # 쿼리 작성: 최근 1주일간의 button_id를 개수로 정렬
    buttons = (
        db.query(ButtonLog.user_id, ButtonLog.category, ButtonLog.button_id, func.count(ButtonLog.button_id).label("count"))
        .filter(ButtonLog.date >= week)
        .filter(ButtonLog.user_id == recommend.user_id)
        .filter(ButtonLog.category == recommend.category)
        .group_by(ButtonLog.button_id)
        .order_by(desc("count"))
        .all()
    )

    result = []
    for i in range(min(5, len(buttons))):
        button = buttons[i]
        button_info = (
            db.query(ButtonList)
            .filter(ButtonList.user_id == recommend.user_id)
            .filter(ButtonList.category == recommend.category)
            .filter(ButtonList.button_id == button.button_id)
            .first()
        )
        if button_info:
            result.append({
                "button_id": button_info.button_id,
                "category": button_info.category,
                "button_text": button_info.button_text,
                "count": button.count
            })

    return result

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

def update_button(db: Session, data: UpdateButton):
    for i in range(len(data.button_text)):
        original_button = (
            db.query(ButtonList)
            .filter(ButtonList.user_id == data.user_id)
            .filter(ButtonList.category == data.category)
            .filter(ButtonList.button_id == i+1)
            .first()
        )

        if original_button and original_button.button_text != data.button_text[i]:
            db.query(ButtonLog).filter(
                ButtonLog.user_id == data.user_id,
                ButtonLog.category == data.category,
                ButtonLog.button_id == i+1
            ).delete()
            
        button = ButtonList(
            user_id=data.user_id,
            button_id=i+1,
            category=data.category,
            button_text=data.button_text[i]
        )
        m_button = db.merge(button)
        db.commit()
        db.refresh(m_button)

    return True

def select_category(db: Session, data: SelectCategory):
    db.query(SelectedCategory).filter(SelectedCategory.user_id == data.user_id).delete()
    db.commit()

    for category in data.category:  # data.categories는 category 리스트라고 가정
        new_row = SelectedCategory(user_id=data.user_id, category=category)
        db.add(new_row)
    db.commit()
    return True

def get_selected_category(db: Session, data: GetSelectedCategory):
    selected_categories = db.query(SelectedCategory).filter(SelectedCategory.user_id == data.user_id).all()
    return [category.category for category in selected_categories]

def get_selected_category_ar(db: Session, data: GetSelectedCategory):
    selected_categories = db.query(SelectedCategory).filter(SelectedCategory.user_id == data.user_id).all()

    category_map = {
        "에어컨": "AirRequestButton",
        "침대": "BedRequestButton",
        "책": "BookRequestButton",
        "의자": "ChairRequestButton",
        "시계": "ClockRequestButton",
        "문": "DoorRequestButton",
        "선풍기": "FanRequestButton",
        "램프": "LampRequestButton",
        "노트북": "LaptopRequestButton",
        "머그컵": "MugRequestButton",
        "체온계": "ThermometerRequestButton",
        "휴지": "TissueRequestButton",
        "창문": "WindowRequestButton",
        "TV": "TVRequestButton",
    }

    return [category_map.get(category.category, category.category) for category in selected_categories]
