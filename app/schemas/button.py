from pydantic import BaseModel
from typing import List, Optional

class ButtonLogAdd(BaseModel):
    user_id: str
    button_id: int
    category: str

class ButtonRecommend(BaseModel):
    user_id: str

class ButtonRecommendByCategory(BaseModel):
    user_id: str
    category: str

class CustomButton(BaseModel):
    user_id: str
    button_id: int
    category: str
    button_text: str

class GetButtonByCategory(BaseModel):
    user_id: str
    category: str

class UpdateButton(BaseModel):
    user_id: str
    button_text: List[str]
    category: str

class SelectCategory(BaseModel):
    user_id: str
    category: List[str]

class GetSelectedCategory(BaseModel):
    user_id: str
