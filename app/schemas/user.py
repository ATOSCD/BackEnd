from pydantic import BaseModel

class UserCreate(BaseModel):
    user_id: str 
    name: str
    password: str