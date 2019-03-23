import sys
import random
import Buffer_sys as Buf


def send_message(vk, data):
    vk.messages.send(peer_id=data['peer_id'],
                     message=data['text'],
                     attachment=','.join(data['attachments']),
                     forward_messages=data['fwd_msg'],
                     )


def greetings(vk, data):
    new_data = {'peer_id': data['peer_id'],
                'text': 'Привет!',
                'attachments': [],
                'fwd_msg': '',
                'user_id': data['user_id'],
                }
    if data['from_chat']:
        new_data['fwd_msg'] = str(data['message_id'])
    send_message(vk, new_data)


def shut_down(vk, data):
    print('Иду на отклю-ючку-у-у...')
    sys.exit()


def random_choose(vk, data):
    new_data = {'peer_id': data['peer_id'],
                'text': '',
                'attachments': [],
                'fwd_msg': '',
                'user_id': data['user_id'],
                }

    try:
        data['text'] = data['text'][5:]
        index = data['text'].find('\n')
        amount = data['text'][:index].strip(' :')
        data['text'] = data['text'][index + 1:]

        array = data['text'].split('\n')
        for choose in array:
            choose.strip()
        choose_array = [x for x in array if x]

        try:
            amount = float(amount)
            if amount % 1 != 0:
                new_data['text'] = 'Число\nДолжно\nБыть\nЦЕЛЫМ! ヽ( `д´*)ノ'
            elif amount < 0:
                new_data['text'] = 'Ну класс! Как я тебе отрицательное кол-во ответов выведу-то? :D'
            elif amount == 0:
                new_data['text'] = 'Чего?! Сам себе 0 элементов выбирай, негодяй! .-.'
            elif amount >= len(array):
                new_data['text'] = 'Ты слышь, я столько не выберу! :0'
            else:
                new_data['text'] = 'Выбор:'
                i = 0
                while i < amount:
                    i += 1
                    new_data['text'] += '\n' + choose_array.pop(random.randrange(0, len(choose_array)))
        except ValueError:
            new_data['text'] = 'Ты в порядке? Нет ты...\nЧисло мне дай! x_x'
    except ValueError:
        new_data['text'] = 'Не, здесь точно что-то не так ( -_-)'

    if data['from_chat']:
        new_data['fwd_msg'] = str(data['message_id'])
    send_message(vk, new_data)


def create_buffer(vk, data):
    new_data = {'peer_id': data['peer_id'],
                'text': '',
                'attachments': [],
                'fwd_msg': '',
                'user_id': data['user_id'],
                }
    if data['user']['status'] == 'god':
        try:
            text = data['text'].split()
            buffer_name = text[2]
            password = text[3]
            media_type = text[4]
            new_data['text'] = Buf.create_buffer(data['user'], buffer_name, password, media_type)
        except KeyError:
            new_data['text'] = 'Ты явно что-то забыл ввести...'
    else:
        new_data['text'] = 'Нет у тебя таких привелегий c:'

    send_message(vk, new_data)


def add_to_buffer(vk, data):
    new_data = {'peer_id': data['peer_id'],
                'text': '',
                'attachments': [],
                'fwd_msg': '',
                'user_id': data['user_id'],
                }
    text = data['text'].split()
    buffer_name = text[1]
    if Buf.check_user_allowed_to_buffer(data['user'], buffer_name):
        new_data['text'] = Buf.add_to_buffer(buffer_name, data)
    else:
        new_data['text'] = 'Сорри, ты накосячил...\nЛибо нет такого буффера, либо не тот пароль, сказать не могу :P'
    send_message(vk, new_data)


def release_from_buffer(vk, data):
    new_data = {'peer_id': data['peer_id'],
                'text': '',
                'attachments': [],
                'fwd_msg': '',
                'user_id': data['user_id'],
                }
    text = data['text'].split()
    buffer_name = text[1]
    if Buf.check_user_allowed_to_buffer(data['user'], buffer_name) or data['user']['status'] == 'god':
        mode = ''
        try:
            mode = text[2].upper()
            number = int(text[3])
            new_data['text'], new_data['attachments'] = \
                Buf.copy_from_buffer(buffer_name,
                                     number,
                                     new_data['attachments'],
                                     data['user']['user_name'],
                                     )
        except ValueError:
            if mode == 'РАНДОМ':
                new_data['text'], new_data['attachments'] = \
                    Buf.random_from_buffer(buffer_name,
                                           new_data['attachments'],
                                           data['user']['user_name'],
                                           )
            else:
                new_data['text'] = 'Не знаю я такого режима!\n' \
                                   'ヽ( `д´*)ノ'

        except IndexError:
            new_data['text'], new_data['attachments'] = \
                Buf.pop_from_buffer(buffer_name, new_data['attachments'], data['user']['user_name'])
    else:
        new_data['text'] = 'Сорри, ты накосячил...\nЛибо нет такого буффера, либо не тот пароль, сказать не могу :P'
    send_message(vk, new_data)


def add_user_to_buffer(vk, data):
    new_data = {'peer_id': data['peer_id'],
                'text': '',
                'attachments': [],
                'fwd_msg': '',
                'user_id': data['user_id'],
                }
    text = data['text'].split()
    buffer_name = text[1]
    password = text[2]
    new_data['text'] = Buf.add_user_to_buffer(data['user'], buffer_name, password)
    send_message(vk, new_data)


def change_buffer_password(vk, data):
    new_data = {'peer_id': data['peer_id'],
                'text': '',
                'attachments': [],
                'fwd_msg': '',
                'user_id': data['user_id'],
                }
    if data['user']['status'] == 'god':
        new_data['text'] = Buf.change_buffer_password(new_data)
    else:
        new_data['text'] = 'Фега ты борзый :0'
    send_message(vk, new_data)


def delete_buffer(vk, data):
    new_data = {'peer_id': data['peer_id'],
                'text': '',
                'attachments': [],
                'fwd_msg': '',
                'user_id': data['user_id'],
                }
    if data['user']['status'] == 'god':
        new_data['text'] = Buf.delete_buffer(data['text'].split()[2])
    else:
        new_data['text'] = 'Нет-нет-нет, тебе нельзя!'
    send_message(vk, new_data)


def info_buffer(vk, data):
    new_data = {'peer_id': data['peer_id'],
                'text': '',
                'attachments': [],
                'fwd_msg': '',
                'user_id': data['user_id'],
                }
    try:
        text = data['text'].split()
        buffer_name = text[2]
        if Buf.check_user_allowed_to_buffer(data['user'], buffer_name):
            new_data['text'] = Buf.buffer_info(buffer_name)
        else:
            new_data['text'] = 'Сорри, ты накосячил...\nЛибо нет такого буффера, либо не тот пароль, сказать не могу :P'
    except KeyError:
        new_data['text'] = 'Чёт данных мало ._.'
    send_message(vk, new_data)


command_base = {'ПРИВЕТ': greetings,
                'ВЫКЛЮЧИСЬ': shut_down,
                'ОФФНИСЬ': shut_down,
                'ВЫБОР': random_choose,
                'СОЗДАЙ БУФФЕР': create_buffer,
                'ДОБАВЬ': add_to_buffer,
                'ОТДАЙ': release_from_buffer,
                'ПРИМИ': add_user_to_buffer,
                'СМЕНИ ПАРОЛЬ': change_buffer_password,
                'УДАЛИ БУФФЕР': delete_buffer,
                'ИНФА БУФФЕР': info_buffer,
                }
