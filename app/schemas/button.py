from pydantic import BaseModel

class ButtonLogAdd(BaseModel):
    user_id: str
    button_id: int

class ButtonRecommend(BaseModel):
    user_id: str

class CustomButton(BaseModel):
    user_id: str
    button_id: int
    category: str
    button_text: str

class GetButtonByCategory(BaseModel):
    user_id: str
    category: str