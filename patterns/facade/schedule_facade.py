from patterns.adapter.adapters import LessonJSONAdapter, ExamJSONAdapter
from patterns.builder.builder import NotificationBuilder
from patterns.template.concrete_downloaders import LessonScheduleDownloader, ExamScheduleDownloader


class ScheduleFacade:
    """
    Facade pentru proces complet: download, parse, adapt, build notificări
    """
    def __init__(self):
        self.lesson_downloader = LessonScheduleDownloader()
        self.exam_downloader = ExamScheduleDownloader()
        self.builder = NotificationBuilder()

    def update_lessons(self, json_path):
        self.lesson_downloader.download()
        adapter = LessonJSONAdapter(json_path)
        records = adapter.get_records()
        messages = []
        for rec in records:
            self.builder.set_lesson(rec)
            messages.append(self.builder.get_message())
        return messages

    def update_exams(self, json_path):
        self.exam_downloader.download()
        adapter = ExamJSONAdapter(json_path)
        records = adapter.get_records()
        messages = []
        for rec in records:
            self.builder.set_exam(rec)
            messages.append(self.builder.get_message())
        return messages