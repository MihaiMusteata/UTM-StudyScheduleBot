from patterns.observer.observer import Observer, Subject

class StudentObserver(Observer):
    def __init__(self, chat_id: int, group_name: str, send_message):
        self.chat_id = chat_id
        self.group_name = group_name
        self.send_message = send_message

    async def update(self, subject: Subject, message: str) -> None:
        await self.send_message(self.chat_id, message)


class TeacherObserver(Observer):
    def __init__(self, chat_id: int, teacher_name: str, send_message):
        self.chat_id = chat_id
        self.teacher_name = teacher_name
        self.send_message = send_message

    async def update(self, subject: Subject, message: str) -> None:
        await self.send_message(self.chat_id, message)