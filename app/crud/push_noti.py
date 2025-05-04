
import json
import requests
from google.oauth2 import service_account
import google.auth.transport.requests
from sqlalchemy.orm import Session
from app.models.FCMToken import FCMToken
from app.models.Notification import Notifications
from dotenv import load_dotenv
import os

load_dotenv()

FCM_SERVER_KEY = os.getenv("FCM_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        FCM_SERVER_KEY,
        scopes=["https://www.googleapis.com/auth/firebase.messaging"]  # FCM API 권한
    )
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)
    return credentials.token

def send_push_message(db: Session, user_id: str, title: str, body: str):
    access_token = get_access_token()
    
    db_token = db.query(FCMToken).filter(FCMToken.user_id == user_id).first()
    if not db_token:
        print(f"FCM 토큰을 찾을 수 없습니다. user_id: {user_id}")
        return

    fcm_token = db_token.token
    print(f"FCM 토큰: {fcm_token}")

    url = f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; UTF-8',
    }

    message = {
        'message': {
            'token': fcm_token,
            'notification': {
                'title': title,
                'body': body,
            },
            'android': {
                'priority': 'high',
            },
            'apns': {
                'headers': {
                    'apns-priority': '10',
                },
                'payload': {
                    'aps': {
                        'content-available': 1,
                    },
                },
            },
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(message))

    if response.status_code == 200:
        print('푸시 알림 전송 성공!')
    else:
        print(f'푸시 알림 전송 실패: {response.status_code}, {response.text}')

def save_token(db: Session, user_id: str, token: str):
    db_token = db.query(FCMToken).filter(FCMToken.user_id == user_id).first()

    if db_token:
        db_token.token = token
        print(f"기존 토큰 업데이트: user_id={user_id}, token={token}")
    else:
        db_token = FCMToken(user_id=user_id, token=token)
        db.add(db_token)
        print(f"새 토큰 저장: user_id={user_id}, token={token}")

    db.commit()
    db.refresh(db_token)
    return db_token

def save_noti_to_db(db: Session, user_id: int, title: str, body: str):
    new_noti = Notifications(
        user_id=user_id,
        title=title,
        body=body
    )
    db.add(new_noti)
    db.commit()
    db.refresh(new_noti)
    return new_noti