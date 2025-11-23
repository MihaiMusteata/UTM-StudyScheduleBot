from telegram import Update
from telegram.ext import ContextTypes
from patterns.command.command import Command


class CommandInvoker:
    def __init__(self):
        self._commands = {}

    def register(self, name: str, command: Command):
        self._commands[name] = command

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        cmd_name = update.message.text.lstrip("/").split()[0]
        command = self._commands.get(cmd_name)
        if command:
            await command.execute(update, context)
        else:
            await update.message.reply_text(f"Unknown command: {cmd_name}")