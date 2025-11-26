from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler

from components.keyboards.subscribe_keyboards import (
    select_study_cycle_keyboard,
    select_year_keyboard,
    groups_keyboard,
    professors_keyboard
)
from patterns.observer.concrete_observers import StudentObserver, TeacherObserver


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, observe_lessons, observe_exams, send_message):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = update.effective_chat.id

    if data == "role_student":
        await query.edit_message_text(
            "Selectează ciclul și forma de învățământ:",
            reply_markup=select_study_cycle_keyboard()
        )

    elif data == "role_professor":
        await query.edit_message_text(
            "Alege profesorul:",
            reply_markup=professors_keyboard()
        )

    elif data in ["cycle_bachelor_fulltime", "cycle_bachelor_lowfreq", "cycle_master"]:
        context.user_data["cycle"] = data
        await query.edit_message_text(
            "Alege anul de studiu:",
            reply_markup=select_year_keyboard(data)
        )

    elif data == "back_to_cycle":
        await query.edit_message_text(
            "Selectează ciclul și forma de învățământ:",
            reply_markup=select_study_cycle_keyboard()
        )

    elif data.startswith(("cycle_bachelor_fulltime_", "cycle_bachelor_lowfreq_", "cycle_master_")):
        year_number = data.split("_")[-1]
        context.user_data["year"] = year_number

        await query.edit_message_text(
            f"Ai ales: Anul {year_number}\n"
            "Acum alege grupa:",
            reply_markup=groups_keyboard("toate")
        )

    elif data.startswith("group_"):
        group = data.replace("group_", "")
        student_observer = StudentObserver(chat_id=chat_id, group_name=group, send_message=send_message)
        observe_lessons.attach(student_observer)
        observe_exams.attach(student_observer)
        context.user_data["group"] = group
        cycle_map = {
            "cycle_bachelor_fulltime": "Licență - învățământ cu frecvență",
            "cycle_bachelor_lowfreq" : "Licență - învățământ cu frecvență redusă",
            "cycle_master" : "Masterat"
        }

        await query.edit_message_text(
            f"Super! Ai ales:\n"
            f"• Ciclu: {cycle_map[context.user_data['cycle']]}\n"
            f"• Anul: {context.user_data.get('year')}\n"
            f"• Grupa: {group}\n\n"
            "Orarul tău va fi trimis în curând sau salvează-ți selecția cu /orar",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Schimbă selecția", callback_data="back_to_cycle")
            ]])
        )

    elif data.startswith("teacher_"):
        prof = data.replace("teacher_", "")
        teacher_observer = TeacherObserver(chat_id=chat_id, teacher_name=prof, send_message=send_message)
        observe_lessons.attach(teacher_observer)
        observe_exams.attach(teacher_observer)
        await query.edit_message_text(
            f"Ai ales profesorul: {prof}\n"
            "Orarul va fi trimis în curând.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Alege alt profesor", callback_data="role_professor")
            ]])
        )


callback_handler = CallbackQueryHandler(handle_callback)