from patterns.composite.component import Component


class LessonLeaf(Component):
    def __init__(self, lesson_info: dict):
        super().__init__()
        self.lesson_info = lesson_info

    def operation(self) -> str:
        grupa_col = next((k for k in self.lesson_info if k.startswith("col_4")), "")
        return f"{self.lesson_info.get('col_3','')} - {self.lesson_info.get(grupa_col,'')}"

class ExamLeaf(Component):
    def __init__(self, exam_info: dict):
        super().__init__()
        self.exam_info = exam_info

    def operation(self) -> str:
        return f"{self.exam_info.get('col_5','')} - {self.exam_info.get('col_2','')} ({self.exam_info.get('col_4','')})"
