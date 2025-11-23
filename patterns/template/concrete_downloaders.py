from patterns.template.pdf_downloader import PDFDownloader


class LessonScheduleDownloader(PDFDownloader):

    def get_url(self) -> str:
        return "https://fcim.utm.md/wp-content/uploads/sites/24/2025/11/orar-master-2025-2026-sem-1-anul-1_final.pdf"

    def get_filename(self) -> str:
        return "master-lessons.pdf"

    def after_download(self, filename: str):
        print("Lesson PDF downloaded.")
        print(f"Saved as {filename}")


class ExamScheduleDownloader(PDFDownloader):

    def get_url(self) -> str:
        return "https://fcim.utm.md/wp-content/uploads/sites/24/2025/10/Sesiuni-de-examinare-Anul-I-semestru-I_2025_2026_P1.pdf"

    def get_filename(self) -> str:
        return "master-exams.pdf"

    def after_download(self, filename: str):
        print("Exam PDF downloaded.")
        print(f"Saved as {filename}")
