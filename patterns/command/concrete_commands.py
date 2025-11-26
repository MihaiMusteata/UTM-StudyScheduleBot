from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from components.keyboards.subscribe_keyboards import role_keyboard
from patterns.command.command import Command

class HelloCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f"Hello {update.effective_user.first_name}")

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
        observe_lessons = context.user_data["observe_lessons"]
        observe_exams = context.user_data["observe_exams"]
        observer = context.user_data["observer"]
        observe_lessons.deattach(observer)
        observe_exams.deattach(observer)

        await update.message.reply_text("Te-ai dezabonat cu succes de la notificări!")

class NotifyCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Notification sent to all subscribers!")
