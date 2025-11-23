from patterns.facade.schedule_facade import ScheduleFacade

if __name__ == "__main__":
    facade = ScheduleFacade()

    print("=== Lessons Notifications ===")
    lesson_messages = facade.update_lessons("master-lessons.json")
    for msg in lesson_messages[:3]:
        print(msg)

    print("=== Exams Notifications ===")
    exam_messages = facade.update_exams("master-exams.json")
    for msg in exam_messages[:3]:
        print(msg)