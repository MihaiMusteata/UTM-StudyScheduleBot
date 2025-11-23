from patterns.builder.concrete_builders import LessonNotificationBuilder, ExamNotificationBuilder
from patterns.builder.director import NotificationDirector

if __name__ == "__main__":
    director = NotificationDirector()

    # ----- Lecție pentru student -----
    lesson_builder = LessonNotificationBuilder()
    director.builder = lesson_builder

    director.build_student_lesson({
        "student": "Grupa TI-231",
        "subject": "Programare",
        "date": "25.11.2025",
        "time": "10:00",
        "room": "A206"
    })

    notif = lesson_builder.notification
    print(notif.render())

    # ----- Examen pentru profesor -----
    exam_builder = ExamNotificationBuilder()
    director.builder = exam_builder

    director.build_professor_lesson({
        "professor": "Prof. Ion Popescu",
        "subject": "Algoritmi",
        "date": "12.01.2026",
        "time": "08:00",
        "room": "B101"
    })

    notif2 = exam_builder.notification
    print(notif2.render())