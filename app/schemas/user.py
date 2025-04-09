from pydantic import BaseModel

class UserCreate(BaseModel):
    user_id: str 
    name: str
    password: str

class SetNok(BaseModel):
    user_id: str
    nok_id: str