from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup


def switch_chat(update, context):
    update.message.reply_text('На кого вы хотите переключить чат?')
    return 1


def chat_switched(update, context):
    message = update.message.text
    with open('bot/logs/names.txt', 'r') as names:
        names = names.read()
        if message in names:
            switch_id_to = names[names.find(message) - 10:names.find(message) - 1]
            update.message.reply_text(f'Вы переключились на чат с {message}.')
            context.user_data['friend'] = switch_id_to
        else:
            update.message.reply_text('Человек не найден!')
    return ConversationHandler.END


def stop(update, context):
    return ConversationHandler.END


def task(context):
    job = context.job
    global length
    with open('bot/logs/from_vk_to_tg.txt', 'r') as logs:
        answers = logs.readlines()
        if len(answers) != length:
            context.bot.send_message(job.context, text=' '.join(answers[0].split()[:-4]))
            length += 1
        if answers:
            answers.pop(0)
            length -= 1
    with open('bot/logs/from_vk_to_tg.txt', 'w') as logs:
        logs.write(''.join(answers))


def send_message(update, context):
    chat_id = update.message.chat_id
    try:
        due = 1
        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()
        new_job = context.job_queue.run_repeating(task, due, context=chat_id)
        context.chat_data['job'] = new_job

    except (IndexError, ValueError):
        pass


def main():
    REQUEST_KWARGS = {
        'proxy_url': 'socks5h://geek:socks@t.geekclass.ru:7777'
    }
    updater = Updater("1156438301:AAFDrWFKvxh3zQFoHWh6trKSii8CVoODdbw", use_context=True,
                      request_kwargs=REQUEST_KWARGS)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, send_message)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('switch', switch_chat)],
        states={
            1: [MessageHandler(Filters.text, chat_switched)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(text_handler)
    print('Telegram bot is started')
    updater.start_polling()
    updater.idle()


length = 0
if __name__ == '__main__':
    main()
