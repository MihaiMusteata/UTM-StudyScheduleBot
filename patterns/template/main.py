from patterns.template.concrete_downloaders import LessonScheduleDownloader, ExamScheduleDownloader

if __name__ == "__main__":
    lesson_downloader = LessonScheduleDownloader()
    exam_downloader = ExamScheduleDownloader()

    lesson_downloader.download()
    exam_downloader.download()