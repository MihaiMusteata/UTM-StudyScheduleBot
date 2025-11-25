import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from global_config import absolute_path


def role_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Student", callback_data="role_student"),
            InlineKeyboardButton("Profesor", callback_data="role_professor")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def select_study_cycle_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔸Ciclul I, Licență - învățământ cu frecvență", callback_data="cycle_bachelor_fulltime")],
        [InlineKeyboardButton("🔹Ciclul I, Licență - învățământ cu frecvență redusă", callback_data="cycle_bachelor_lowfreq")],
        [InlineKeyboardButton("🎓Ciclu II, Masterat", callback_data="cycle_master")],
    ]
    return InlineKeyboardMarkup(keyboard)

def select_year_keyboard(cycle_type: str) -> InlineKeyboardMarkup:
    if cycle_type == "cycle_bachelor_fulltime":
        years = ["Anul I", "Anul II", "Anul III", "Anul IV"]
    elif cycle_type == "cycle_bachelor_lowfreq":
        years = ["Anul I", "Anul II", "Anul III", "Anul IV", "Anul V"]
    elif cycle_type == "cycle_master":
        years = ["Anul I", "Anul II"]
    else:
        return InlineKeyboardMarkup([])

    callback_prefix = cycle_type + "_"
    keyboard = []
    for year in years:
        callback = f"{callback_prefix}{year.split()[-1]}"
        keyboard.append([InlineKeyboardButton(year, callback_data=callback)])

    keyboard.append([InlineKeyboardButton("Înapoi la cicluri", callback_data="back_to_cycle")])

    return InlineKeyboardMarkup(keyboard)


def groups_keyboard(category: str):
    groups = []
    with open(absolute_path + "/patterns/adapter/groups.json", "r", encoding="utf-8") as f:
        groups = json.load(f)
    keyboard = [[InlineKeyboardButton(g, callback_data=f"group_{g}")] for g in groups]
    return InlineKeyboardMarkup(keyboard) if groups else None


def professors_keyboard():
    professors = []
    with open(absolute_path + "/patterns/adapter/professors.json", "r", encoding="utf-8") as f:
        professors = json.load(f)
    keyboard = [[InlineKeyboardButton(p, callback_data=f"teacher_{p}")] for p in professors]
    return InlineKeyboardMarkup(keyboard)