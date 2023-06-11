from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def create_keyboard(list_button: list[str, int], one_time=False) -> object:
    '''Example: ['btn_red', 'red', 'btn_blue', 'blue', 0, 'btn_green', 'green']

    this example will create two buttons side by side and one below

    :param list_button: "button name", "button color", but only between buttons there can be a line break "0" int.
    :param one_time: disappears after click.
    :return: object keyboard.
    '''
    key_view = VkKeyboard(one_time)

    flag_button_or_color = True
    list_btn = []
    list_color = []
    for i in list_button:
        if i == 0:
            list_btn.append(0)
            list_color.append(0)
            continue
        else:
            if flag_button_or_color:
                list_btn.append(i)
                flag_button_or_color = not flag_button_or_color
            else:
                if i == "red":
                    list_color.append(VkKeyboardColor.NEGATIVE)
                elif i == 'green':
                    list_color.append(VkKeyboardColor.POSITIVE)
                elif i == 'blue':
                    list_color.append(VkKeyboardColor.PRIMARY)
                elif i == 'white':
                    list_color.append(VkKeyboardColor.SECONDARY)
                flag_button_or_color = not flag_button_or_color

    for button, color in zip(list_btn, list_color):
        if button == 0:
            key_view.add_line()
            continue
        else:
            key_view.add_button(button, color)

    return key_view.get_keyboard()
