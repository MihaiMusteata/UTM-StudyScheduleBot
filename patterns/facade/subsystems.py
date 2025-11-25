import asyncio
import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler

from components.handlers.callback_handlers import callback_handler
from patterns.adapter.adapters import LessonJSONAdapter, ExamJSONAdapter
from patterns.command.concrete_commands import HelloCommand, SubscribeCommand, UnsubscribeCommand, NotifyCommand
from patterns.command.invoker import CommandInvoker
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
        self.invoker = CommandInvoker()
        self.app = None

    async def generic_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.invoker.handle(update, context)

    def init_bot(self):
        self.invoker.register("hello", HelloCommand())
        self.invoker.register("subscribe", SubscribeCommand())
        self.invoker.register("unsubscribe", UnsubscribeCommand())
        self.invoker.register("notify", NotifyCommand())
        print("TelegramSubsystem: Initializing Telegram bot...")

    async def start_bot(self):
        print("TelegramSubsystem: Starting Telegram bot...")

        self.app = ApplicationBuilder().token(self.token).build()

        self.app.add_handler(CommandHandler(["hello", "subscribe", "unsubscribe", "notify"], self.generic_handler))
        self.app.add_handler(callback_handler)

        await self.app.initialize()
        await self.app.start()
        print("TelegramSubsystem: Bot running with polling...")
        await self.app.updater.start_polling()
        try:
            while True:
                await asyncio.sleep(3600)
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            await self.app.updater.stop()
            await self.app.stop()
            await self.app.shutdown()

    async def send_message(self, chat_id: int, text: str):
        if not self.app:
            raise Exception("Telegram bot is not running. Call operation_z first.")

        await self.app.bot.send_message(chat_id=chat_id, text=text)

# --------------------------
# Subsystem 4 – Background service
# --------------------------
class BackgroundServiceSubsystem:
    def __init__(self):
        self.URL = "https://fcim.utm.md/procesul-de-studii/orar/#toggle-id-3"
        self.STATE_FILE = "schedule_monitor_state.json"
        self.running = False
        self.monitor_task = None

    async def _check_for_changes(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [Monitor] Performing scheduled check...")
        try:
            current_state = self._fetch_current_schedule_links()
            previous_state = self._load_previous_state()

            if previous_state is None:
                print(f"[{datetime.now().strftime('%H:%M')}] [Monitor] First run – initial state saved.")
                self._save_current_state(current_state)
                return

            lessons_changed = current_state["lessons"] != previous_state["lessons"]
            exams_changed = current_state["exams"] != previous_state["exams"]

            if lessons_changed:
                print(f"[{datetime.now().strftime('%H:%M')}] LESSONS: UPDATED")
                #TODO Notify

            if exams_changed:
                print(f"[{datetime.now().strftime('%H:%M')}] EXAMS: UPDATED")
                #TODO Notify

            if lessons_changed or exams_changed:
                self._save_current_state(current_state)

        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M')}] [Monitor] Error during check: {e}")

    def _fetch_current_schedule_links(self):
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ScheduleMonitorBot/1.0)"}
        response = requests.get(self.URL, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        tbody = soup.select_one("#toggle-id-3 tbody")
        if not tbody:
            raise ValueError("Could not find schedule table on the page.")

        rows = tbody.find_all("tr")[1:]  # Skip header row (Calendarul universitar)

        lessons = {"year1": None, "year2": None}
        exams = {"year1": None, "year2": None}

        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 3:
                continue

            title = cells[0].get_text(strip=True).lower()
            link_year1 = cells[1].find("a")["href"] if cells[1].find("a") else None
            link_year2 = cells[2].find("a")["href"] if cells[2].find("a") else None

            if "activități didactice" in title or "orar activități" in title:
                lessons["year1"] = link_year1
                lessons["year2"] = link_year2
            elif "sesiune de examinare" in title and "reexaminare" not in title:
                exams["year1"] = link_year1
                exams["year2"] = link_year2

        return {"lessons": lessons, "exams": exams}

    def _load_previous_state(self):
        if not os.path.exists(self.STATE_FILE):
            return None
        try:
            with open(self.STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def _save_current_state(self, state):
        with open(self.STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)


    async def start_monitoring(self):
        if self.running:
            print("BackgroundServiceSubsystem: Already running.")
            return

        self.running = True
        print("BackgroundServiceSubsystem: Schedule monitoring started (checks every hour)")

        await self._check_for_changes()

        while self.running:
            await asyncio.sleep(3600)
            await self._check_for_changes()

    def stop_monitoring(self):
        self.running = False
        print("BackgroundServiceSubsystem: Monitoring stopped.")

    def create_background_task(self, loop=None):
        loop = loop or asyncio.get_event_loop()
        self.monitor_task = loop.create_task(self.start_monitoring())
        return self.monitor_task