from sqlalchemy.orm import Session
from app.models.RecommendText import *
from jamo import h2j, j2hcj

def add_recommend_texts(db: Session, recommend_texts: list):
    for text in recommend_texts:
        db_recommend_text = RecommendChat(recommend_text=text)
        db.add(db_recommend_text)
    db.commit()
    db.refresh(db_recommend_text)
    return db_recommend_text

def update_recommend_texts(db: Session, user_id: str, recommend_texts: list):
    return 0


def get_recommend_texts(db: Session, user_id: str, input_text: str):
    sentence_list = db.query(RecommendChat).all()
    sentence_list = [sentence.recommend_text for sentence in sentence_list]
    results = []

    for sentence in sentence_list:
        if is_jamo_substring(input_text, sentence):
            results.append(sentence)
        if len(results) >= 4:
            break
        
    return results


def is_jamo_substring(short, long):
    # 한글을 자모로 분리
    short_jamo = j2hcj(h2j(short)).replace(" ", "")
    long_jamo = j2hcj(h2j(long)).replace(" ", "")
    if short_jamo in long_jamo:
        print(f"'{short_jamo}' is a substring of '{long_jamo}'")
    return short_jamo in long_jamo