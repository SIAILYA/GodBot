from panel import app
from bot import bot
from multiprocessing import Process


if __name__ == '__main__':
    app_process = Process(target=app.main)
    bot_process = Process(target=bot.GodBotVk)

    app_process.start()
    bot_process.start()