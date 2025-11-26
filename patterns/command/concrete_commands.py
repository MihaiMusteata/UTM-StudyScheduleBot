import json
from asyncio import sleep

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

from components.keyboards.subscribe_keyboards import role_keyboard
from global_config import absolute_path
from patterns.builder.concrete_builders import LessonNotificationBuilder, ExamNotificationBuilder
from patterns.builder.director import NotificationDirector
from patterns.command.command import Command

class StartCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Bine ai venit la botul de orar!\n"
        )

class SubscribeCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Te rog să alegi cine ești:",
            reply_markup=role_keyboard())

class UnsubscribeCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            observer = context.user_data["observer"]
        except KeyError:
            observer = None

        if observer is None:
            await update.message.reply_text("Nu ești abonat la nicio notificare.")
            return

        observe_lessons = context.user_data["observe_lessons"]
        observe_exams = context.user_data["observe_exams"]

        observe_lessons.detach(observer)
        observe_exams.detach(observer)

        await update.message.reply_text("Te-ai dezabonat cu succes de la notificări!")

class ShowLessonsScheduleCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        director = NotificationDirector()
        lesson_builder = LessonNotificationBuilder()
        director.builder = lesson_builder
        try:
            observer = context.user_data["observer"]
        except KeyError:
            observer = None

        if observer is None:
            await update.message.reply_text(
                "Nu ești abonat la orarul lecțiilor.\n"
                "Folosește /subscribe pentru a te abona."
            )
            return

        with open(absolute_path + "/patterns/adapter/lessons-schedule.json", "r", encoding="utf-8") as f:
            lessons = json.load(f)

        await update.message.reply_text("Orarul lecțiilor:\n\n")

        try:
            if observer.group_name is not None:
                for lesson in lessons:
                    if lesson['student_group'] == observer.group_name:
                        director.build_student_message(lesson)
                        message = lesson_builder.notification.render()
                        await update.message.reply_text(message)
                        await sleep(1)
        except AttributeError:
            pass

        try:
            if observer.teacher_name is not None:
                for lesson in lessons:
                    if lesson['professor'] == observer.teacher_name:
                        director.build_professor_message(lesson)
                        message = lesson_builder.notification.render()
                        await update.message.reply_text(message)
                        await sleep(1)
        except AttributeError:
            pass

class ShowExamsScheduleCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        director = NotificationDirector()
        exam_builder = ExamNotificationBuilder()
        director.builder = exam_builder
        try:
            observer = context.user_data["observer"]
        except KeyError:
            observer = None

        if observer is None:
            await update.message.reply_text(
                "Nu ești abonat la orarul examenelor.\n"
                "Folosește /subscribe pentru a te abona."
            )

            return

        with open(absolute_path + "/patterns/adapter/exams-schedule.json", "r", encoding="utf-8") as f:
            exams = json.load(f)

        await update.message.reply_text("Orarul Examenelor:\n\n")
        flag = True

        try:
            if observer.group_name is not None:
                for exam in exams:
                    if observer.group_name in exam['student_group'] :
                        director.build_student_message(exam)
                        message = exam_builder.notification.render()
                        flag = False
                        await update.message.reply_text(message)
                        await sleep(1)
            if flag:
                await update.message.reply_text("Nu există examene programate pentru grupa ta.")
        except AttributeError:
            pass

        try:
            if observer.teacher_name is not None:
                for lesson in exams:
                    if lesson['professor'] in observer.teacher_name:
                        director.build_professor_message(lesson)
                        message = exam_builder.notification.render()
                        flag = False
                        await update.message.reply_text(message)
                        await sleep(1)
            if flag:
                await update.message.reply_text("Nu există examene programate pentru discplina ta.")
        except AttributeError:
            pass


class MenuCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        menu_text = (
            "📋 <b>Meniu Principal</b>\n\n"
            "Bun venit! Alege o opțiune din lista de mai jos:\n\n"
            "🔔 <b>Activează notificările</b>\n"
            "   /subscribe — Primești alerte automate pentru lecții și examene\n\n"
            "🔕 <b>Dezactivează notificările</b>\n"
            "   /unsubscribe — Oprești toate notificările automate\n\n"
            "📚 <b>Orarul lecțiilor</b>\n"
            "   /orar_lectii — Vezi programul complet al cursurilor\n\n"
            "📝 <b>Orarul examenelor</b>\n"
            "   /orar_examene — Consultă calendarul sesiunii\n\n"
            "🏠 <b>Afișează meniul</b>\n"
            "   /menu — Revino la acest meniu oricând\n\n"
            "💡 <i>Apasă pe comandă sau folosește butoanele de mai jos</i>"
        )

        await update.message.reply_text(menu_text, parse_mode="HTML")

