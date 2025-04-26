from pydantic import BaseModel

class NotificationRequest(BaseModel):
    user_id: str
    title: str
    body: str

class TokenData(BaseModel):
    user_id: str
    token: str