from pydantic import BaseModel

class TextRecommend(BaseModel):
    user_id: str
    input_text: str