from pydantic import BaseModel
from datetime import datetime

class NotificationRequest(BaseModel):
    user_id: str
    title: str
    body: str

class TokenData(BaseModel):
    user_id: str
    token: str

class NotificationResponse(BaseModel):
    id: int
    user_id: str
    title: str
    body: str
    created_at: datetime

