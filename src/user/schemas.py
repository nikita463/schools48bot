from pydantic import BaseModel

class User(BaseModel):
    tg_id: int
    tg_username: str
    v_token: str
    student_name: str
