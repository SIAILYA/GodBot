from bot.stat_updater import updater
from panel import app
from bot.bot import main as mainVK
from bot.tg_bot import main as mainTG
from bot.checker import main as mainChecker
from multiprocessing import Process

__VERSION__ = '1.0'

if __name__ == '__main__':
    panel_process = Process(target=app.main)
    VK_process = Process(target=mainVK)
    VK_loader_process = Process(target=mainChecker)
    TG_process = Process(target=mainTG)
    stat_updater = Process(target=updater)

    VK_process.start()
    panel_process.start()
    TG_process.start()
    stat_updater.start()
    VK_loader_process.start()
