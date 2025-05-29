from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    user_id: str 
    name: str
    password: str
    patient : int # 1: 보호자, 2: 환자

class SetNok(BaseModel):
    user_id: str
    nok_id: str

class GetNok(BaseModel):
    user_id: str

class FindUser(BaseModel):
    user_id: str
    password: str

class ReturnUser(BaseModel):
    user_id: str
    name: str
    nok_id: Optional[str] = None
    patient: int

class Userlogin(BaseModel):
    user_id: str
    password: str

class IdCheck(BaseModel):
    user_id: str

