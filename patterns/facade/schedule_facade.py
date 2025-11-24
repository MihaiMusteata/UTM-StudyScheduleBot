from patterns.facade.subsystems import LessonSubsystem, TelegramSubsystem, ExamSubsystem

class ScheduleFacade:
    def __init__(self):
        self._lessons = LessonSubsystem()
        self._exams = ExamSubsystem()
        self._telegram = TelegramSubsystem()

    def update_lessons(self, json_path):
        print(self._lessons.run_lesson())
        records = self._lessons.download_lesson(json_path)

    def update_exams(self, json_path):
        print(self._exams.run_exam())
        records = self._exams.download_exam(json_path)

    def start_bot(self):
        print(self._telegram.init_bot())
        self._telegram.start_bot()
    #
    # async def send_notification(self, chat_id: int, message: str):
    #     await self._telegram.send_message(chat_id, message)
