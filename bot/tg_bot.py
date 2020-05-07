from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup


def start(update, context):
    reply_keyboard = [['Зайти в музей']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!',
                              reply_markup=markup)


def way(update, context):
    answer = update.message.text
    print(answer)
    update.message.reply_text('Вы вошли в первый зал. Здесь представлены популярнейшие скульптуры из глины: вазы,'
                              ' кувшины, тарелки и столовые приборы, на стенах висят инструменты.')


def main():
    REQUEST_KWARGS = {
        'proxy_url': 'socks5h://geek:socks@t.geekclass.ru:7777'
    }
    updater = Updater("1156438301:AAFDrWFKvxh3zQFoHWh6trKSii8CVoODdbw", use_context=True,
                      request_kwargs=REQUEST_KWARGS)
    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, way)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(text_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
