from patterns.observer.concrete_observers import LessonsSchedule, ExamsSchedule
from patterns.observer.observer import Observer, Subject

class StudentObserver(Observer):
    def __init__(self, chat_id: int, group_name: str):
        self.chat_id = chat_id
        self.group_name = group_name

    async def update(self, subject: Subject) -> None:
        messages = []
        if isinstance(subject, LessonsSchedule):
            for row in subject.data[1:]:  # sărim header
                for key, value in subject.data[0].items():
                    if value.strip() == self.group_name:
                        cell = row.get(key, "").strip()
                        if cell:
                            messages.append(f"Lecție: {cell}")
        elif isinstance(subject, ExamsSchedule):
            for row in subject.data[1:]:
                if row.get("col_4") == self.group_name:
                    messages.append(f"Examen: {row.get('col_2')} cu {row.get('col_3')} la {row.get('col_5')} {row.get('col_6')} sala {row.get('col_7')}")

        # for msg in messages:
        #     await app.bot.send_message(chat_id=self.chat_id, text=msg)


class TeacherObserver(Observer):
    def __init__(self, chat_id: int, teacher_name: str):
        self.chat_id = chat_id
        self.teacher_name = teacher_name

    async def update(self, subject: Subject) -> None:
        messages = []
        if isinstance(subject, LessonsSchedule):
            header = subject.data[0]
            group_cols = {k: v for k, v in header.items() if k.startswith("col_") and v not in ["Data","ora","Ziua",""]}

            for row in subject.data[1:]:
                for col_key, group_name in group_cols.items():
                    cell = row.get(col_key,"").strip()
                    if self.teacher_name in cell:
                        messages.append(f"Lecție cu {self.teacher_name}: {cell} (grupa {group_name})")
        elif isinstance(subject, ExamsSchedule):
            for row in subject.data[1:]:
                if row.get("col_3") == self.teacher_name:
                    messages.append(f"Examen cu {self.teacher_name}: {row.get('col_2')} grupa {row.get('col_4')} la {row.get('col_5')} {row.get('col_6')} sala {row.get('col_7')}")

        # for msg in messages:
        #     await app.bot.send_message(chat_id=self.chat_id, text=msg)