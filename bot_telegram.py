import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler

import oge_parser

logging.basicConfig(
    filename='log_oge_results.txt',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO

)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Привет, {update.message.from_user.first_name}\! \nЧтобы получить результаты, "
                                        "отправьте данные в следующем формате: \n"
                                        "_Иванов 4019 112233_", parse_mode="MarkdownV2")


async def getResults(update: Update, context: ContextTypes.DEFAULT_TYPE):
    surname, series, number = update.message.text.split(" ")
    print(f'{surname} {series} {number} {update.message.from_user.full_name}')
    try:
        results = oge_parser.OGE(surname, series, number).value
    except ValueError:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="В базе совпадений не найдено.\nОтправь снова, прочитав еще раз :)\nБот ссылается на ege.spb.ru!\n")
    else:
        s = ""
        for one_result in results:
            s += f'{one_result["subject"]} -> {one_result["mark"]}\n'
        # print(results)

        await context.bot.send_message(chat_id=update.effective_chat.id, text=s)


if __name__ == '__main__':
    application = ApplicationBuilder().token('5395167161:AAH8xa8wSZRyP2TfMS_62X-EOqPa-sUvDOI').build()

    start_handler = CommandHandler('start', start)
    getResults_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), getResults)
    application.add_handler(start_handler)
    application.add_handler(getResults_handler)

    application.run_polling()