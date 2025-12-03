from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class UserOrm(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(primary_key=True)
    tg_username: Mapped[str]
    v_token: Mapped[str]
    student_name: Mapped[str]
