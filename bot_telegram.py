import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO

)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Введи фамилию одноклассника"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="||пошел нахуй||",
        parse_mode="MarkdownV2"
    )
    message = f'{update.message.text} — {update.message.from_user.full_name}'
    print(message)
    f = open("log.txt", "a")
    f.write(f'{message}\n')
    f.close()


if __name__ == '__main__':
    application = ApplicationBuilder().token('5395167161:AAH8xa8wSZRyP2TfMS_62X-EOqPa-sUvDOI').build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()
