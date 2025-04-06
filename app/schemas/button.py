from pydantic import BaseModel

class ButtonLogAdd(BaseModel):
    user_id: str
    button_id: int

class ButtonRecommend(BaseModel):
    user_id: str