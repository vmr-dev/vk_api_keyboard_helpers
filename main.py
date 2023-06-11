import time

import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType

from vk_keyboard_helpers import create_keyboard
from config import TOKEN


def get_username(vk_user_id: int) -> str:
    user_get = vk.users.get(user_ids=vk_user_id)
    user_get = user_get[0]
    first_name = user_get['first_name']
    last_name = user_get['last_name']
    full_name = f"{first_name} {last_name}"

    return full_name


def send_personal_message(recipient_id, message_content, keyboard_object=None) -> None:
    vk_session.method('messages.send',
                      {'user_id': recipient_id, 'message': message_content, 'random_id': time.time(),
                       'keyboard': keyboard_object})


def send_group_message(recipient_id, message_content,
                       keyboard_object=None) -> None:
    vk_session.method('messages.send',
                      {'chat_id': recipient_id, 'message': message_content, 'random_id': time.time(),
                       'keyboard': keyboard_object})


vk_session = vk_api.VkApi(token=TOKEN)
LongPoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

print('[Start Project Py.]')

for event in LongPoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text
        user_id = event.user_id
        username = get_username(user_id)

        try:
            inv = event.raw[6]['source_act']
            user_id_invite = event.raw[6]['source_mid']
            username_invite = get_username(user_id_invite)
            # New user invitation >>>
            if inv == 'chat_invite_user':
                send_group_message(event.chat_id, f"Welcome! @id{user_id_invite} ({username_invite})")
            # Kick user >>>
            elif inv == 'chat_kick_user':
                send_group_message(event.chat_id, f"Goodbye! @id{user_id_invite} ({username_invite})")
        except KeyError or AttributeError:
            pass

        # Personal chat >>>
        try:
            chat_id = event.chat_id
        except AttributeError:
            list_button_and_color = ['start', 'green', 'stop', 'red', 0, 'exit', 'blue']
            send_personal_message(user_id, f'{get_username(user_id)} hey! I`m bot for chat.)',
                                  create_keyboard(list_button_and_color))
            continue

        # Group chat >>>
        if text:
            print(user_id)
            send_group_message(chat_id, f'@id{user_id}({get_username(user_id)}):  {text}')
