from telegram import Update
from telegram.ext import ContextTypes
from patterns.command.command import Command

class HelloCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f"Hello {update.effective_user.first_name}")

class SubscribeCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user.username or update.effective_user.first_name
        await update.message.reply_text(f"{user} subscribed to notifications!")

class UnsubscribeCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user.username or update.effective_user.first_name
        await update.message.reply_text(f"{user} unsubscribed from notifications!")

class NotifyCommand(Command):
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Notification sent to all subscribers!")
