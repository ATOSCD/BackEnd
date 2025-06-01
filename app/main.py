from fastapi import FastAPI, Request, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .database.connection import SessionLocal, engine, Base
from .crud.user import *
from .crud.button import *
from .crud.chat import *
from .crud.push_noti import *
from .crud.text_recommend import *
from .config import SWAGGER_HEADERS, swagger_ui_parameters
from .schemas.user import *
from .schemas.button import *
from .schemas.chat import *
from .schemas.notification import *
from .schemas.text_recommend import *
from typing import List
import asyncio

# DB 테이블 생성 (최초 실행 시 필요)
Base.metadata.create_all(bind=engine)

app = FastAPI(swagger_ui_parameters=swagger_ui_parameters, **SWAGGER_HEADERS)

templates = Jinja2Templates(directory="app/templates")

# 의존성 주입: DB 세션 가져오기
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def update_recommend_chat():
    while True:
        print("주기적으로 실행되는 작업입니다.")
        # 여기에 원하는 작업(예: DB 업데이트 등) 작성
        await asyncio.sleep(60)  # 60초마다 실행

@app.on_event("startup")
async def start_periodic_task():
    asyncio.create_task(update_recommend_chat())

# FastAPI 기본 경로
@app.get("/", response_class=HTMLResponse, description="서버 기본 경로", tags=["Root"])
def read_root(request: Request):
    return templates.TemplateResponse("root.html", {"request": request})

# 로그인 API
@app.post("/login/", description="로그인", tags=["User"])
def login(user: Userlogin, db: Session = Depends(get_db)):
    return user_login(db, user)

# 아이디 중복 체크 API
@app.post("/check-id/", description="아이디 중복 체크", tags=["User"])
def check_id(user: IdCheck, db: Session = Depends(get_db)):
    return id_check(db, user)

# 사용자 추가 API
@app.post("/add-user/", description="사용자 추가", tags=["User"])
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

# 모든 사용자 조회 API
@app.get("/get-users/", description="모든 사용자 조회", tags=["User"])
def read_users(db: Session = Depends(get_db)):
    return get_users(db)

# 사용자 조회 API
@app.post("/find-patient/", description="사용자 조회", tags=["User"])
def read_user(dto: FindUser, db: Session = Depends(get_db)):
    return find_patient(db, dto)
    

@app.post("/set-nok/", description="NOK ID 설정", tags=["User"])
def set_nok(dto: SetNok, db: Session = Depends(get_db)):
    return set_nok_id(db, dto)

@app.post("/get-nok/", description="NOK ID 조회", tags=["User"])
def get_nok(dto: GetNok, db: Session = Depends(get_db)):
    return get_nok_id(db, dto)

# 버튼 커스텀
@app.post("/custom-button/", description="버튼 커스텀", tags=["Button"])
def custom_buttons(data: CustomButton, db: Session = Depends(get_db)):
    return custom_button(db, data)

# 버튼 업데이트 API
@app.post("/update-button/", description="버튼 업데이트", tags=["Button"])
def update_buttons(data: UpdateButton, db: Session = Depends(get_db)):
    return update_button(db, data)

# 버튼 카테고리별 조회 API
@app.post("/get-button-by-category/", description="카테고리별 버튼 조회", tags=["Button"])
def get_buttons_by_category(data: GetButtonByCategory, db: Session = Depends(get_db)):
    return get_button_by_category(db, data)

# 버튼 로그 추가 API
@app.post("/add-button-log/", description="버튼 클릭 로그 추가", tags=["Button"])
def button_log_add(button_log: ButtonLogAdd, db: Session = Depends(get_db)):
    return add_button_log(db, button_log)

@app.post("/recommned-cateogry/", description="카테고리 사용량 증가", tags=["Recommend"])
def recommend_categories(request: GetSelectedCategory, db: Session = Depends(get_db)):
    return recommend_category(db, request.user_id)

# # 버튼 추천 API (category별)
# @app.post("/recommend-button-by-category/", description="카테고리별 버튼 추천 (최근 1주일 가장 많은 순서대로 리턴)", tags=["Button"])
# def button_recommend_category(recommend: ButtonRecommendByCategory, db: Session = Depends(get_db)):
#     return recommend_buttons_by_category(db, recommend)

# # 버튼 추천 API (전체)
# @app.post("/recommend-button/", description="버튼 추천 (최근 1주일 가장 많은 순서대로 리턴)", tags=["Button"])
# def button_recommend(recommend: ButtonRecommend, db: Session = Depends(get_db)):
#     return recommend_buttons(db, recommend)

# 버튼 카테고리 선택 (목을 움직이는 환자를 위한 기능)
@app.post("/select-button-category/", description="버튼 카테고리 선택", tags=["Button"])
def select_button_category(data: SelectCategory, db: Session = Depends(get_db)):
    return select_category(db, data)

# 선택된 카테고리 조회 API
@app.post("/get-selected-category/", description="선택된 카테고리 조회", tags=["Button"])
def get_selected_categories(data: GetSelectedCategory, db: Session = Depends(get_db)):
    return get_selected_category(db, data)

# 선택된 카테고리 조회 API (AR 용)
@app.post("/get-selected-category-ar/", description="선택된 카테고리 조회 (AR 용)", tags=["Button"])
def get_selected_categories_ar(data: GetSelectedCategory, db: Session = Depends(get_db)):
    return get_selected_category_ar(db, data)

# 채팅 테스트 페이지
@app.get("/ws/chat-test", response_class=HTMLResponse, description="채팅 테스트", tags=["Chat"])
def chat_test(request: Request):
    return templates.TemplateResponse("chat_test.html", {"request": request})

# 채팅 테스트 페이지
@app.get("/ws/iot-test", response_class=HTMLResponse, description="IoT 테스트", tags=["IoT"])
def iot_test(request: Request):
    return templates.TemplateResponse("iot_test.html", {"request": request})

# 채팅 조회 API
@app.get("/get-messages/{user_id}/", description="채팅방 메시지 조회", tags=["Chat"])
def read_messages(user_id: str, db: Session = Depends(get_db)):
    return get_messages(db, user_id)

# 웹소켓 채팅 API
connected_clients: dict = {}
@app.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket, db: Session = Depends(get_db)):
    user_id = websocket.query_params.get("user_id")
    connected_clients[user_id] = websocket  
    if not user_id:
        await websocket.close(code=1008, reason="user_id is required")
        return
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            nok = get_nok_id(db, GetNok(user_id=user_id)) 
            if not nok:
                await websocket.close(code=1008, reason="NOK ID not found")
                return
            to_whom = nok["nok_id"] 
            save_message_to_db(db, user_id=user_id, to_whom=to_whom, content=message)
            user = get_user(db, user_id)
            await multicast_message([to_whom,user_id], {"user_id": user_id, "user_name": user.name, "message": message}, connected_clients)
    except WebSocketDisconnect:
        connected_clients.pop(websocket)

async def multicast_message(to_send, data: dict, connected: dict):
    for user_id in to_send:
        print(f"Sending message to {user_id}: {data}")
        ws = connected.get(user_id)
        if ws:
            try:
                await ws.send_json(data)
            except Exception as e:
                print(f"Failed to send message to {user_id}: {e}")


connected_recommend: dict = {}
@app.websocket("/ws/chat-recommend")
async def chat_websocket(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_json()
            user_id = message.get("user_id")
            text = message.get("text")
            connected_recommend[user_id] = websocket  
            recommend_text = get_recommend_texts(db, user_id, text)
            await unicast_message(user_id, {"user_id": user_id, "text": recommend_text}, connected_recommend)
    except WebSocketDisconnect:
        connected_recommend.pop(user_id, None)

async def unicast_message(user_id, data: dict, connected: dict):
    ws = connected.get(user_id)
    if ws:
        try:
            await ws.send_json(data)
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")


# IoT 웹소켓 통신 API
connected_IoTs: List[WebSocket] = []
@app.websocket("/ws/iot")
async def iot_websocket(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    connected_IoTs.append(websocket)
    try:
        while True:
            message = await websocket.receive_json()
            iot_id = message.get("iot_id")
            content = message.get("message")

            if not iot_id:
                await websocket.close(code=1008, reason="iot_id is required in the message")
                return

            print(f"Received from IoT {iot_id}: {content}")
            await broadcast_message_iot({"iot_id": iot_id, "message": content})
    except WebSocketDisconnect:
        connected_IoTs.remove(websocket)

async def broadcast_message_iot(data: dict):
    for client in connected_IoTs:
        try:
            await client.send_json(data)
        except Exception as e:
            print(f"Failed to send message to IoT : {e}")


# FCM 푸시 알림 전송 API
@app.post("/send-notification/", description="알림 전송 (Unity에서 호출)", tags=["Notification"])
async def send_notification(request: NotificationRequest, db: Session = Depends(get_db)):
    send_push_message(db, request.user_id, request.title, request.body)
    save_noti_to_db(db, request.user_id, request.title, request.body)
    increase_category_usage(db, request.user_id, request.category)
    return {"message": "푸시 알림 전송 요청 완료"}

# 긴급 알림 전송 API
@app.post("/send-emergency-notification/", description="긴급 알림 전송 (Unity에서 호출)", tags=["Notification"])
async def send_emergency_notification(request: NotificationRequest, db: Session = Depends(get_db)):
    send_push_warning(db, request.user_id, request.title, request.body)
    save_noti_to_db(db, request.user_id, request.title, request.body)
    return {"message": "긴급 푸시 알림 전송 요청 완료"}

# 알림 조회 API
@app.get("/get-notifications/{user_id}/", description="알림 조회", tags=["Notification"], response_model=List[NotificationResponse])
async def get_notifications(user_id: str, db: Session = Depends(get_db)):
    notifications = get_noti(db, user_id)
    return notifications

@app.post("/register-token/", description="FCM 토큰 저장", tags=["Notification"])
async def register_token(data: TokenData, db: Session = Depends(get_db)):
    save_token(db, data.user_id, data.token)
    return {"message": "토큰 등록 완료"}

@app.post("/save-notification/", description="알림 저장", tags=["Notification"])
async def save_notification(request: NotificationRequest, db: Session = Depends(get_db)):
    save_noti_to_db(db, request.user_id, request.title, request.body)
    return {"message": "알림 저장 완료"}

# 채팅 추천 추가 API
@app.post("/add-recommend-chat/", description="추천 채팅 추가", tags=["RecommendChat"])
def add_recommend_chat(recommend_texts: List[str], db: Session = Depends(get_db)):
    return add_recommend_texts(db, recommend_texts)

# 채팅 추천 조회 API
@app.post("/get-recommend-chat/", description="추천 채팅 조회", tags=["RecommendChat"])
def get_recommend_chat(data: TextRecommend, db: Session = Depends(get_db)):
    return get_recommend_texts(db, data.user_id, data.input_text)