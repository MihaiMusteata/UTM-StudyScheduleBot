from patterns.facade.subsystems import LessonSubsystem, TelegramSubsystem, ExamSubsystem, BackgroundServiceSubsystem
from patterns.observer.concrete_subjects import LessonsSchedule, ExamsSchedule


class ScheduleFacade:
    def __init__(self, app):
        self._lessons = LessonSubsystem()
        self._exams = ExamSubsystem()
        self.observe_lessons = LessonsSchedule(app)
        self.observe_exams = ExamsSchedule()
        self._telegram = TelegramSubsystem(app, self.observe_lessons, self.observe_exams)
        self._monitor = BackgroundServiceSubsystem(self.observe_lessons, self.observe_exams)


    def update_lessons(self, json_path):
        print(self._lessons.run_lesson())
        records = self._lessons.download_lesson(json_path)

    def update_exams(self, json_path):
        print(self._exams.run_exam())
        records = self._exams.download_exam(json_path)

    async def start_bot(self):
        print(self._telegram.init_bot())
        await self._telegram.start_bot()

    async def start_background_monitoring(self):
        print("Starting background schedule monitoring (every hour)...")
        self._monitor.create_background_task()

    def stop_background_monitoring(self):
        self._monitor.stop_monitoring()
