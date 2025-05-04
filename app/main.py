from fastapi import FastAPI, Request, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .database.connection import SessionLocal, engine, Base
from .models.User import User
from .models.Chat import Message
from .crud.user import *
from .crud.button import *
from .crud.chat import *
from .crud.push_noti import *
from .config import SWAGGER_HEADERS, swagger_ui_parameters
from .schemas.user import *
from .schemas.button import *
from .schemas.chat import *
from .schemas.notification import *
from .chat.save_chat import save_message_to_db
from typing import List



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

# FastAPI 기본 경로
@app.get("/", response_class=HTMLResponse, description="서버 기본 경로", tags=["Root"])
def read_root(request: Request):
    return templates.TemplateResponse("root.html", {"request": request})

# 사용자 추가 API
@app.post("/add-user/", description="사용자 추가", tags=["User"])
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

# 모든 사용자 조회 API
@app.get("/get-users/", description="모든 사용자 조회", tags=["User"])
def read_users(db: Session = Depends(get_db)):
    return get_users(db)

@app.post("/set-nok/", description="NOK ID 설정", tags=["User"])
def set_nok(dto: SetNok, db: Session = Depends(get_db)):
    return set_nok_id(db, dto)

# 버튼 로그 추가 API
@app.post("/add-button-log/", description="버튼 클릭 로그 추가", tags=["Button"])
def button_log_add(button_log: ButtonLogAdd, db: Session = Depends(get_db)):
    return add_button_log(db, button_log)

# 버튼 추천 API
@app.post("/recommend-button/", description="버튼 추천 (최근 1주일 가장 많은 순서대로 리턴)", tags=["Button"])
def button_recommend(recommend: ButtonRecommend, db: Session = Depends(get_db)):
    return recommend_buttons(db, recommend)

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
connected_clients: List[WebSocket] = []
@app.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket, db: Session = Depends(get_db)):
    user_id = websocket.query_params.get("user_id")
    if not user_id:
        await websocket.close(code=1008, reason="user_id is required")
        return
    
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            save_message_to_db(db, user_id=user_id, content=message)
            await broadcast_message({"user_id": user_id, "message": message})
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def broadcast_message(data: dict):
    for client in connected_clients:
        try:
            await client.send_json(data)
        except Exception as e:
            print(f"Failed to send message to {client}: {e}")


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
    return {"message": "푸시 알림 전송 요청 완료"}

@app.post("/register-token/", description="FCM 토큰 저장", tags=["Notification"])
async def register_token(data: TokenData, db: Session = Depends(get_db)):
    save_token(db, data.user_id, data.token)
    return {"message": "토큰 등록 완료"}