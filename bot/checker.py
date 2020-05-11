from bot.api import VkApi
from time import sleep


def main():
    print('VK checker is started!')
    length = 0
    while True:
        sleep(1)
        with open(r'C:\Projects\GodBot\bot\logs\from_tg_to_vk.txt', 'r') as logs:
            answers = logs.readlines()
            if len(answers) != length:
                answer = answers[0].split()
                VkApi().message_send(int(answer[0]), ' '.join(answer[1:-4]))
                length += 1
            if answers:
                answers.pop(0)
                length -= 1
        with open(r'C:\Projects\GodBot\bot\logs\from_tg_to_vk.txt', 'w') as logs:
            logs.write(''.join(answers))