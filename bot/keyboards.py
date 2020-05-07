from vk_api.keyboard import VkKeyboardColor, VkKeyboard


def kick_keyboard(kick_id):
    keyboard = VkKeyboard(inline=True)
    keyboard.add_button('Выгнать', color=VkKeyboardColor.NEGATIVE, payload=[f'kick {kick_id}'])
    return keyboard.get_keyboard()
