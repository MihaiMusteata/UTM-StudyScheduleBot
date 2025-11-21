import json
from strategy import ScheduleContext
from student_lessons_strategy import StudentLessonsStrategy
from student_exams_strategy import StudentExamsStrategy
from teacher_lessons_strategy import TeacherLessonsStrategy
from teacher_exams_strategy import TeacherExamsStrategy

def load_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    context = ScheduleContext(StudentLessonsStrategy("TI-251M"))
    schedule = context.process(load_json("../factory_method/master-lessons.json"))

    with open("TI-251M-lessons-schedule.json", "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)
    print(schedule)

    context.strategy = TeacherLessonsStrategy()
    teachers = context.process(load_json("../factory_method/master-lessons.json"))

    with open("Teachers-schedule.json", "w", encoding="utf-8") as f:
        json.dump(teachers, f, ensure_ascii=False, indent=2)
    print(teachers)

    context = ScheduleContext(StudentExamsStrategy("TIA-241M"))
    exams_student = context.process(load_json("../factory_method/master-exams.json"))

    with open("TIA-241M-exams-schedule.json", "w", encoding="utf-8") as f:
        json.dump(exams_student, f, ensure_ascii=False, indent=2)
    print(exams_student)

    context.strategy = TeacherExamsStrategy("A. Leahu")
    exams_teacher = context.process(load_json("../factory_method/master-exams.json"))

    with open("Leahu Alexei - exams-schedule.json", "w", encoding="utf-8") as f:
        json.dump(exams_teacher, f, ensure_ascii=False, indent=2)
    print(exams_teacher)
