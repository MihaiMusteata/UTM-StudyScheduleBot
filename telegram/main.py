from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

# async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text(f'Hello {update.effective_user.first_name}')
#
# load_dotenv()
#
# BOT_TOKEN = os.getenv("BOT_TOKEN")
#
# print(BOT_TOKEN)
# app = ApplicationBuilder().token(BOT_TOKEN).build()
#
# app.add_handler(CommandHandler("hello", hello))
#
# app.run_polling()

from patterns.facade.schedule_facade import ScheduleFacade

if __name__ == "__main__":
    facade = ScheduleFacade()

    facade.start_bot()