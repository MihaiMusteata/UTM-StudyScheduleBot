import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler

from patterns.adapter.adapters import LessonJSONAdapter, ExamJSONAdapter
from patterns.builder.builder import NotificationBuilder
from patterns.template.concrete_downloaders import LessonScheduleDownloader, ExamScheduleDownloader


# --------------------------
# Subsystem 1 – Lessons
# --------------------------
class LessonSubsystem:
    def __init__(self):
        self.downloader = LessonScheduleDownloader()

    def run_lesson(self):
        return "Running LessonSubsystem..."


    def download_lesson(self, json_path):
        self.downloader.download()
        adapter = LessonJSONAdapter(json_path)
        return adapter.get_records()


# --------------------------
# Subsystem 2 – Exams
# --------------------------
class ExamSubsystem:
    def __init__(self):
        self.downloader = ExamScheduleDownloader()

    def run_exam(self):
        return "Running ExamSubsystem..."

    def download_exam(self, json_path):
        self.downloader.download()
        adapter = ExamJSONAdapter(json_path)
        return adapter.get_records()

# --------------------------
# Subsystem 3 – Telegram Bot
# --------------------------
class TelegramSubsystem:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("BOT_TOKEN")
        self.app = None

    def init_bot(self):
        print("TelegramSubsystem: Initializing Telegram bot...")

    async def command_hello(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Hello {update.effective_user.first_name}')

    def start_bot(self):
        print("TelegramSubsystem: Starting Telegram bot...")

        self.app = ApplicationBuilder().token(self.token).build()

        self.app.add_handler(CommandHandler("hello", self.command_hello))

        print("TelegramSubsystem: Bot running with polling...")
        self.app.run_polling()

    async def send_message(self, chat_id: int, text: str):
        if not self.app:
            raise Exception("Telegram bot is not running. Call operation_z first.")

        await self.app.bot.send_message(chat_id=chat_id, text=text)
