from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

from components.keyboards.subscribe_keyboards import role_keyboard
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

class MenuCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        menu_text = (
            "Meniu Principal\n\n"
            "Alege ce vrei să faci:\n\n"
            "/subscribe - Primește notificări – vei fi anunțat despre orarul lecțiilor și examenelor\n"
            "/unsubscribe - Oprește notificările – te dezabonezi complet\n"
            "/menu - Accesează meniul – reafișează acest meniu oricând\n\n"
            "Apasă butonul dorit mai jos!"
        )

        await update.message.reply_text(menu_text)

