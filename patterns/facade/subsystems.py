import asyncio
import json
import os
from datetime import datetime, timedelta
from functools import partial

import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

from components.handlers.callback_handlers import handle_callback
from global_config import absolute_path
from patterns.adapter.adapters import LessonJSONAdapter, ExamJSONAdapter
from patterns.command.concrete_commands import SubscribeCommand, UnsubscribeCommand, StartCommand, MenuCommand, \
    ShowLessonsScheduleCommand, ShowExamsScheduleCommand, GetScheduleForTodayCommand, GetScheduleForTodayCommand, \
    GetScheduleForTomorrowCommand, ScheduleService, GetScheduleForThisWeekCommand, GetScheduleForNextWeekCommand
from patterns.command.invoker import CommandInvoker
from patterns.observer.concrete_subjects import LessonsSchedule, ExamsSchedule
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
    def __init__(self, app, observe_lessons: LessonsSchedule, observe_exams: ExamsSchedule):
        self.invoker = CommandInvoker()
        self.app = app
        self.observe_lessons = observe_lessons
        self.observe_exams = observe_exams

    async def generic_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.invoker.handle(update, context)

    def init_bot(self):
        schedule_service = ScheduleService()
        self.invoker.register("start", StartCommand())
        self.invoker.register("subscribe", SubscribeCommand())
        self.invoker.register("unsubscribe", UnsubscribeCommand())
        self.invoker.register("menu", MenuCommand())
        self.invoker.register("orar_lectii", ShowLessonsScheduleCommand())
        self.invoker.register("orar_examene", ShowExamsScheduleCommand())
        self.invoker.register("azi", GetScheduleForTodayCommand(schedule_service))
        self.invoker.register("maine", GetScheduleForTomorrowCommand(schedule_service))
        self.invoker.register("saptamana_curenta", GetScheduleForThisWeekCommand(schedule_service))
        self.invoker.register("saptamana_viitoare", GetScheduleForNextWeekCommand(schedule_service))

        print("TelegramSubsystem: Initializing Telegram bot...")

    async def send_message(self, chat_id: int, text: str):
        if not self.app:
            raise Exception("Telegram bot is not running. Call operation_z first.")
        await self.app.bot.send_message(chat_id=chat_id, text=text)


    async def start_bot(self):
        print("TelegramSubsystem: Starting Telegram bot...")

        self.app.add_handler(CommandHandler([
            "start",
            "subscribe",
            "unsubscribe",
            "menu",
            "orar_lectii",
            "orar_examene",
            "azi",
            "maine",
            "saptamana_curenta",
            "saptamana_viitoare"
        ], self.generic_handler))
        callback_handler_func = partial(
            handle_callback,
            observe_lessons=self.observe_lessons,
            observe_exams=self.observe_exams,
            send_message=self.send_message
        )

        self.app.add_handler(CallbackQueryHandler(callback_handler_func))
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

# --------------------------
# Subsystem 4 – Background service
# --------------------------
class BackgroundServiceSubsystem:
    def __init__(self, observe_lessons: LessonsSchedule, observe_exams: ExamsSchedule):
        self.URL = "https://fcim.utm.md/procesul-de-studii/orar/#toggle-id-3"
        self.STATE_FILE = "schedule_monitor_state.json"
        self.REMINDER_STATE_FILE = "reminders_state.json"

        self.running = False
        self.monitor_task = None
        self.reminder_task = None

        self.observe_lessons = observe_lessons
        self.observe_exams = observe_exams
        self.lessons_path = f"{absolute_path}/patterns/adapter/lessons-schedule.json"
        self.exams_path = f"{absolute_path}/patterns/adapter/exams-schedule.json"

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
                self.observe_lessons.update_schedule("Orarul lecțiilor a fost actualizat.")

            if exams_changed:
                print(f"[{datetime.now().strftime('%H:%M')}] EXAMS: UPDATED")
                self.observe_exams.update_schedule("Orarul examenelor a fost actualizat.")

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

        rows = tbody.find_all("tr")[1:]

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

    def _load_lessons(self):
        with open(self.lessons_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_exams(self):
        with open(self.exams_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _parse_lesson_start_time(self, lesson):
        first_range = lesson["time"].split()[0]
        start_time = first_range.split("-")[0]
        return datetime.strptime(start_time, "%H:%M").time()

    def _parse_exam_start_time(self, exam):
        return datetime.strptime(exam["time"], "%H:%M").time()

    def _is_lesson_today(self, lesson):
        period, weekday_part = lesson["date"].split(" (")
        weekday = weekday_part.replace(")", "")
        start_str, end_str = period.split("-")
        start = datetime.strptime(start_str, "%d.%m.%Y").date()
        end = datetime.strptime(end_str, "%d.%m.%Y").date()

        today = datetime.now().date()
        today_name = datetime.now().strftime("%A")

        days_map = {
            "Monday": "Luni", "Tuesday": "Marți", "Wednesday": "Miercuri",
            "Thursday": "Joi", "Friday": "Vineri",
            "Saturday": "Sâmbătă", "Sunday": "Duminică"
        }

        return start <= today <= end and days_map[today_name] == weekday

    def _is_exam_today(self, exam):
        exam_date = datetime.strptime(exam["date"], "%d/%m/%y").date()
        return exam_date == datetime.now().date()

    async def _check_upcoming_events(self):
        print("[Reminder] Checking for upcoming events...")
        now = datetime.now()
        now_plus_15 = now + timedelta(minutes=15)

        lessons = self._load_lessons()
        exams = self._load_exams()

        for lesson in lessons:
            if not self._is_lesson_today(lesson):
                continue

            start_time = self._parse_lesson_start_time(lesson)
            lesson_dt = datetime.combine(now.date(), start_time)

            if now <= lesson_dt <= now_plus_15:
                msg = f"⏰ Lecție la {lesson['subject']} începe în 15 minute!\nSala: {lesson['room']}"
                self.observe_lessons.update_schedule(msg)

        for exam in exams:
            if not self._is_exam_today(exam):
                continue

            start_time = self._parse_exam_start_time(exam)
            exam_dt = datetime.combine(now.date(), start_time)

            if now <= exam_dt <= now_plus_15:
                msg = (f"📝 Examen la {exam['subject']} începe în 15 minute!\n"
                       f"Profesor: {exam['professor']} • Sala: {exam['room']}")
                self.observe_exams.update_schedule(msg)


    async def start_reminder_service(self):
        print("[Reminder] Reminder service started (checks every 60 sec)")
        while self.running:
            try:
                await self._check_upcoming_events()
            except Exception as e:
                print("[Reminder] Error:", e)

            await asyncio.sleep(10)

    async def start_monitoring(self):
        if self.running:
            print("BackgroundServiceSubsystem: Already running.")
            return

        self.running = True
        print("BackgroundServiceSubsystem: Schedule monitoring started")

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
        self.reminder_task = loop.create_task(self.start_reminder_service())
        return self.monitor_task, self.reminder_task