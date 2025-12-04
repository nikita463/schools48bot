from typing import Any, Dict
from pydantic import BaseModel, Field
import datetime as dt


Json = Dict[str, Any]


class File(BaseModel):
    filename: str = ""
    link: str = ""


class Homework(BaseModel):
    id: int = 0
    text: str = ""
    individual: bool = False
    files: list[File] = Field(default_factory=list)


class Lesson(BaseModel):
    name: str = ""
    date: dt.date = dt.date(2000, 1, 1)
    homeworks: list[Homework] = Field(default_factory=list)
    id: int = 0
    num: str = 0
    room: str = ""
    teacher: str = ""
    topic: str = ""
    start: dt.time | None = None
    end: dt.time | None = None


class Day(BaseModel):
    date: dt.date = dt.date(2000, 1, 1)
    title: str = ""
    lessons: list[Lesson] = Field(default_factory=list)


class Student(BaseModel):
    name: str = ""
    title: str = ""
    days: list[Day] = Field(default_factory=list)


class Vendor(BaseModel):
    vendor_id: int = 0
    vendor_title: str = ""
    vendor: str = ""
    token: str = ""
    user_title: str = ""
    expires: str = ""
    login: str = ""
    student_name: str = ""
    tg_id: int = 0
