from panel import app
from bot.bot import main as mainVK
from bot.tg_bot import main as mainTG
from bot.checker import main as mainChecker
from multiprocessing import Process

__VERSION__ = '0.2'

if __name__ == '__main__':
    # panel_process = Process(target=app.main)
    VK_process = Process(target=mainVK)
    VK_loader_process = Process(target=mainChecker)
    TG_process = Process(target=mainTG)

    VK_process.start()
    # panel_process.start()
    TG_process.start()
    VK_loader_process.start()
