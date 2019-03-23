import Logs_2 as Log
import os
from Commands_2 import command_base
from Quest_sys import quest_commands
from vk_api.longpoll import VkEventType

name_base = ['БОТ',
             'ЭШЛИ',
             ]


def collect_data(event, vk):
    if event.type == VkEventType.MESSAGE_NEW:
        message = vk.messages.getById(message_ids=event.message_id)['items'][0]
        data = {'peer_id': event.peer_id,
                'text': message['text'],
                'time': event.timestamp,
                'attachments': message['attachments'],
                'fwd_messages': message['fwd_messages'],
                'user_id': message['from_id'],
                'message_id': event.message_id,
                'from_chat': False,
                'command': '',
                'user': '',
                }

        if not os.path.isfile('Users_2\\' + str(data['user_id']) + '.txt'):
            Log.new_user(vk, data['user_id'])
        user = Log.get_user(str(data['user_id']))
        data['user'] = user

        if event.to_me:
            if event.from_chat:
                react, data['text'] = search_appeal(data['text'])
                data['from_chat'] = True
            elif event.from_user:
                react, data['text'] = search_appeal(data['text'])
                react = True
            else:
                react = False

            if react:
                if user['is_quest']:
                    data['command'] = get_quest_command(data['text'])
                else:
                    data['command'] = get_command(data['text'])
    else:
        data = None

    return data


def get_command(text):
    text = text.upper()
    for item in command_base:
        if text.startswith(item):
            print('Команда:', item)
            return item
    return ''


def get_quest_command(text):
    text = text.upper()
    for item in quest_commands:
        if text.startswith(item):
            print('Команда:', item)
            return item
    try:
        int(text)
        return 'ВЫБОР'
    except ValueError:
        pass
    return ''


def search_appeal(text):
    log = False
    copy = text
    text = text.upper()
    for name in name_base:
        if text.startswith(name):
            copy = copy[len(name):].strip(' !.,\n')
            log = True
            break
    return log, copy
