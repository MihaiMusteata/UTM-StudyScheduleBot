from datetime import datetime, timedelta
import json
from asyncio import sleep

from telegram import Update
from telegram.ext import ContextTypes

from components.keyboards.subscribe_keyboards import role_keyboard
from global_config import absolute_path
from patterns.builder.concrete_builders import LessonNotificationBuilder, ExamNotificationBuilder
from patterns.builder.director import NotificationDirector
from patterns.command.command import Command


class StartCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Bine ai venit la botul de orar!\n")


class SubscribeCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Te rog să alegi cine ești:", reply_markup=role_keyboard())


class UnsubscribeCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        observer = context.user_data.get("observer")

        if observer is None:
            await update.message.reply_text("Nu ești abonat la nicio notificare.")
            return

        context.user_data["observe_lessons"].detach(observer)
        context.user_data["observe_exams"].detach(observer)
        await update.message.reply_text("Te-ai dezabonat cu succes de la notificări!")


class ShowLessonsScheduleCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        observer = context.user_data.get("observer")

        if observer is None:
            await update.message.reply_text(
                "Nu ești abonat la orarul lecțiilor.\n"
                "Folosește /subscribe pentru a te abona."
            )
            return

        with open(f"{absolute_path}/patterns/adapter/lessons-schedule.json", "r", encoding="utf-8") as f:
            lessons = json.load(f)

        await update.message.reply_text("Orarul lecțiilor:\n\n")

        director = NotificationDirector()
        lesson_builder = LessonNotificationBuilder()
        director.builder = lesson_builder

        if hasattr(observer, 'group_name') and observer.group_name:
            for lesson in lessons:
                if lesson['student_group'] == observer.group_name:
                    director.build_student_message(lesson)
                    await update.message.reply_text(lesson_builder.notification.render())
                    await sleep(1)

        if hasattr(observer, 'teacher_name') and observer.teacher_name:
            for lesson in lessons:
                if lesson['professor'] == observer.teacher_name:
                    director.build_professor_message(lesson)
                    await update.message.reply_text(lesson_builder.notification.render())
                    await sleep(1)


class ShowExamsScheduleCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        observer = context.user_data.get("observer")

        if observer is None:
            await update.message.reply_text(
                "Nu ești abonat la orarul examenelor.\n"
                "Folosește /subscribe pentru a te abona."
            )
            return

        with open(f"{absolute_path}/patterns/adapter/exams-schedule.json", "r", encoding="utf-8") as f:
            exams = json.load(f)

        await update.message.reply_text("Orarul Examenelor:\n\n")

        director = NotificationDirector()
        exam_builder = ExamNotificationBuilder()
        director.builder = exam_builder
        has_exams = False

        if hasattr(observer, 'group_name') and observer.group_name:
            for exam in exams:
                if observer.group_name in exam['student_group']:
                    director.build_student_message(exam)
                    await update.message.reply_text(exam_builder.notification.render())
                    await sleep(1)
                    has_exams = True

            if not has_exams:
                await update.message.reply_text("Nu există examene programate pentru grupa ta.")

        if hasattr(observer, 'teacher_name') and observer.teacher_name:
            has_exams = False
            for exam in exams:
                if exam['professor'] in observer.teacher_name:
                    director.build_professor_message(exam)
                    await update.message.reply_text(exam_builder.notification.render())
                    await sleep(1)
                    has_exams = True

            if not has_exams:
                await update.message.reply_text("Nu există examene programate pentru disciplina ta.")


class MenuCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        menu_text = (
            "📋 <b>Meniu Principal</b>\n\n"
            "Bun venit! Alege o opțiune din lista de mai jos:\n\n"
            "🔔 <b>Activează notificările</b>\n"
            "   /subscribe — Primești alerte automate pentru lecții și examene\n\n"
            "🔕 <b>Dezactivează notificările</b>\n"
            "   /unsubscribe — Oprești toate notificările automate\n\n"
            "📅 <b>Orarul zilnic</b>\n"
            "   /azi — Vezi orarul pentru astăzi\n"
            "   /maine — Vezi orarul pentru mâine\n\n"
            "📆 <b>Orarul săptămânal</b>\n"
            "   /saptamana_curenta — Vezi orarul pentru săptămâna curentă\n"
            "   /saptamana_viitoare — Vezi orarul pentru săptămâna viitoare\n\n"
            "📚 <b>Orar complet lecții</b>\n"
            "   /orar_lectii — Vezi programul complet al cursurilor\n\n"
            "📝 <b>Orar examene</b>\n"
            "   /orar_examene — Consultă calendarul sesiunii\n\n"
            "🏠 <b>Afișează meniul</b>\n"
            "   /menu — Revino la acest meniu oricând\n\n"
            "💡 <i>Apasă pe comandă sau folosește butoanele de mai jos</i>"
        )
        await update.message.reply_text(menu_text, parse_mode="HTML")


class ScheduleService:
    def __init__(self):
        self.lessons_path = f"{absolute_path}/patterns/adapter/lessons-schedule.json"
        self.exams_path = f"{absolute_path}/patterns/adapter/exams-schedule.json"
        self.days_map = {
            "Monday": "Luni",
            "Tuesday": "Marți",
            "Wednesday": "Miercuri",
            "Thursday": "Joi",
            "Friday": "Vineri",
            "Saturday": "Sâmbătă",
            "Sunday": "Duminică"
        }

    def _load_data(self):
        with open(self.lessons_path, "r", encoding="utf-8") as f:
            lessons = json.load(f)
        with open(self.exams_path, "r", encoding="utf-8") as f:
            exams = json.load(f)
        return lessons, exams

    def _is_lesson_on_date(self, lesson, target_date, day_name):
        date_field = lesson['date']
        parts = date_field.split(" (")
        period = parts[0]
        lesson_day = parts[1].rstrip(")")

        start_date_str, end_date_str = period.split("-")
        start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
        end_date = datetime.strptime(end_date_str, "%d.%m.%Y")

        return start_date.date() <= target_date <= end_date.date() and lesson_day == day_name

    def _is_exam_on_date(self, exam, target_date):
        return datetime.strptime(exam["date"], "%d/%m/%y").date() == target_date

    def get_schedule_for_date(self, target_date, observer):
        lessons, exams = self._load_data()
        day_name = self.days_map[target_date.strftime("%A")]
        filtered_lessons = []
        filtered_exams = []

        if hasattr(observer, 'group_name') and observer.group_name:
            filtered_lessons.extend(
                ('student', lesson) for lesson in lessons
                if lesson['student_group'] == observer.group_name and
                self._is_lesson_on_date(lesson, target_date.date(), day_name)
            )
            filtered_exams.extend(
                ('student', exam) for exam in exams
                if self._is_exam_on_date(exam, target_date.date()) and
                observer.group_name in exam['student_group']
            )

        if hasattr(observer, 'teacher_name') and observer.teacher_name:
            filtered_lessons.extend(
                ('professor', lesson) for lesson in lessons
                if lesson['professor'] == observer.teacher_name and
                self._is_lesson_on_date(lesson, target_date.date(), day_name)
            )
            filtered_exams.extend(
                ('professor', exam) for exam in exams
                if self._is_exam_on_date(exam, target_date.date()) and
                exam['professor'] == observer.teacher_name
            )

        return {
            'lessons': filtered_lessons,
            'exams': filtered_exams,
            'date': target_date,
            'day_name': day_name
        }

    def get_schedule_for_week(self, start_date, observer):
        week_schedule = []
        for i in range(7):
            date = start_date + timedelta(days=i)
            schedule = self.get_schedule_for_date(date, observer)
            if schedule['lessons'] or schedule['exams']:
                week_schedule.append(schedule)
        return week_schedule


async def send_schedule_messages(update, director, schedule_data):
    date_str = schedule_data['date'].strftime("%d.%m.%Y")
    day_name = schedule_data['day_name']

    if not schedule_data['lessons'] and not schedule_data['exams']:
        await update.message.reply_text(
            f"📅 {day_name}, {date_str}\n\n"
            "Nu ai activități programate în această zi."
        )
        return

    await update.message.reply_text(f"📅 Orarul pentru {day_name}, {date_str}:\n")

    lesson_builder = LessonNotificationBuilder()
    director.builder = lesson_builder

    for user_type, lesson in schedule_data['lessons']:
        if user_type == 'student':
            director.build_student_message(lesson)
        else:
            director.build_professor_message(lesson)
        await update.message.reply_text(lesson_builder.notification.render())
        await sleep(0.5)

    exam_builder = ExamNotificationBuilder()
    director.builder = exam_builder

    for user_type, exam in schedule_data['exams']:
        if user_type == 'student':
            director.build_student_message(exam)
        else:
            director.build_professor_message(exam)
        await update.message.reply_text(exam_builder.notification.render())
        await sleep(0.5)


class GetScheduleForTodayCommand(Command):
    def __init__(self, schedule_service):
        self.schedule_service = schedule_service

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        observer = context.user_data.get("observer")

        if observer is None:
            await update.message.reply_text(
                "Nu ești abonat la orarul lecțiilor.\n"
                "Folosește /subscribe pentru a te abona."
            )
            return

        schedule_data = self.schedule_service.get_schedule_for_date(datetime.now(), observer)
        await send_schedule_messages(update, NotificationDirector(), schedule_data)


class GetScheduleForTomorrowCommand(Command):
    def __init__(self, schedule_service):
        self.schedule_service = schedule_service

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        observer = context.user_data.get("observer")

        if observer is None:
            await update.message.reply_text(
                "Nu ești abonat la orarul lecțiilor.\n"
                "Folosește /subscribe pentru a te abona."
            )
            return

        tomorrow = datetime.now() + timedelta(days=1)
        schedule_data = self.schedule_service.get_schedule_for_date(tomorrow, observer)
        await send_schedule_messages(update, NotificationDirector(), schedule_data)


class GetScheduleForThisWeekCommand(Command):
    def __init__(self, schedule_service):
        self.schedule_service = schedule_service

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        observer = context.user_data.get("observer")

        if observer is None:
            await update.message.reply_text(
                "Nu ești abonat la orarul lecțiilor.\n"
                "Folosește /subscribe pentru a te abona."
            )
            return

        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        week_schedule = self.schedule_service.get_schedule_for_week(start_of_week, observer)

        if not week_schedule:
            await update.message.reply_text("Nu ai activități programate în această săptămână.")
            return

        await update.message.reply_text("📅 Orarul pentru săptămâna curentă:\n")

        director = NotificationDirector()
        for schedule_data in week_schedule:
            await send_schedule_messages(update, director, schedule_data)
            await sleep(1)


class GetScheduleForNextWeekCommand(Command):
    def __init__(self, schedule_service):
        self.schedule_service = schedule_service

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        observer = context.user_data.get("observer")

        if observer is None:
            await update.message.reply_text(
                "Nu ești abonat la orarul lecțiilor.\n"
                "Folosește /subscribe pentru a te abona."
            )
            return

        today = datetime.now()
        start_of_next_week = today - timedelta(days=today.weekday()) + timedelta(weeks=1)
        week_schedule = self.schedule_service.get_schedule_for_week(start_of_next_week, observer)

        if not week_schedule:
            await update.message.reply_text("Nu ai activități programate săptămâna viitoare.")
            return

        await update.message.reply_text("📅 Orarul pentru săptămâna viitoare:\n")

        director = NotificationDirector()
        for schedule_data in week_schedule:
            await send_schedule_messages(update, director, schedule_data)
            await sleep(1)