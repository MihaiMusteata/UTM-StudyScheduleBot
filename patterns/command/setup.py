# async def generic_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await invoker.handle(update, context)
#
# invoker = CommandInvoker()
# invoker.register("hello", HelloCommand())
# invoker.register("subscribe", SubscribeCommand())
# invoker.register("unsubscribe", UnsubscribeCommand())
# invoker.register("notify", NotifyCommand())
#
# app = ApplicationBuilder().token(BOT_TOKEN).build()
#
# # folosește un singur handler generic pentru toate comenzile
# app.add_handler(CommandHandler(["hello", "subscribe", "unsubscribe", "notify"], generic_handler))
#
# print("Bot started...")
# app.run_polling()