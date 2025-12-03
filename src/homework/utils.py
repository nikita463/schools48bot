from src.api import Student, Lesson, Vendor
from src.updates import weeks_diary


def get_student_homeworks_list(student: Student) -> list[Lesson]:
    result: list[Lesson] = []
    for day in student.days:
        for lesson in day.lessons:
            if len(lesson.homeworks) > 0:
                result.append(lesson)
    return result


def get_homeworks_list(vendor: Vendor) -> list[Lesson]:
    homeworks_list: list[Lesson] = get_student_homeworks_list(weeks_diary[vendor.tg_id][vendor.student_name])
    return homeworks_list
