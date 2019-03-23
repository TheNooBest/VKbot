import os
import json
import random
import Logs_2 as Log


def check_buffer_password(buffer_name, password):
    path = 'Buffers_2\\{}.txt'.format(buffer_name)
    if os.path.isfile(path):
        file = open(path, mode='r', encoding='UTF-8')
        buffer_data = json.load(file)
        file.close()

        return password == buffer_data['password']
    return False


def check_user_allowed_to_buffer(user, buffer_name):
    for buffer in user['buffers']:
        if buffer == buffer_name:
            return True
    return False


# -----===== LOGIN USER TO BUFFER =====-----
def add_user_to_buffer(user, buffer_name, password):
    if check_user_allowed_to_buffer(user, buffer_name):
        text = 'Ты уже имеешь доступ, дружок-пирожок :3'
    elif check_buffer_password(buffer_name, password):
        user['buffers'].append(buffer_name)
        text = 'Вэлком ту зэ клаб, бадди B-/\n*Звуки неистового шлепка*'
        Log.update_user(user)
    else:
        text = 'Сорри, ты накосячил...\nЛибо нет такого буффера, либо не тот пароль, сказать не могу :P'
    return text


# -----===== CREATE NEW BUFFER =====-----
def create_buffer(user, buffer_name, password, media_type):
    if os.path.isfile('Buffers_2\\' + buffer_name + '.txt'):
        text = 'Звиняй, такое название уже занято :P'
    elif any(media_type == s for s in allowed_media):
        buffer_data = {'password': password,
                       'media_type': media_type,
                       'index': 0,
                       'media_list': [],
                       }
        file = open('Buffers_2\\' + buffer_name + '.txt', mode='w', encoding='UTF-8')
        json.dump(buffer_data, file)
        file.close()

        user['buffers'].append(buffer_name)
        Log.update_user(user)

        text = 'Усё успешно сделано!'
    else:
        text = 'Я так смотрю...\n' \
               'У тебя какой-то неправильный тип вложений :0'
    return text


# -----===== ADD NEW MEDIA TO BUFFER =====-----
def add_to_buffer(buffer_name, data):
    file = open('Buffers_2\\' + buffer_name + '.txt', mode='r', encoding='UTF-8')
    buffer_data = json.load(file)
    file.close()
    i = 0
    if buffer_data['media_type'] == 'text':
        text_ = ''.join(data['text'].split('\n')[1:])
        buffer_data['media_list'].append(text_)
        i += 1
        text = 'Произошло добавление в буффер, {}~'.format(data['user']['user_name'])
    else:
        for attach in data['attachments']:
            a_type = attach['type']
            if a_type == buffer_data['media_type'] or buffer_data['media_type'] == 'all':
                text = '{}{}_{}'.format(a_type, attach[a_type]['owner_id'], attach[a_type]['id'])
                try:
                    access_key = attach[a_type]['access_key']
                    text += '_{}'.format(access_key)
                except KeyError:
                    pass
                buffer_data['media_list'].append(text)
                i += 1
        text = 'Произошло добавление в буффер, {}~\n\n' \
               'Добавлено [{}] из [{}]'.format(data['user']['user_name'], i, len(data['attachments']))

    file = open('Buffers_2\\{}.txt'.format(buffer_name), mode='w', encoding='UTF-8')
    json.dump(buffer_data, file)
    file.close()

    return text


# -----===== GET MEDIA FROM BUFFER =====-----
def pop_from_buffer(buffer_name, attachments, user_name):
    file = open('Buffers_2\\{}.txt'.format(buffer_name), mode='r', encoding='UTF-8')
    buffer_data = json.load(file)
    file.close()

    length = len(buffer_data['media_list'])
    if length > 0:
        if buffer_data['media_type'] == 'text':
            text = 'Ваш текст:\n\n' + buffer_data['media_list'][buffer_data['index']]
        else:
            attachments.append(buffer_data['media_list'][buffer_data['index']])
            text = 'Ваше вложение, {}'.format(user_name)
        buffer_data['index'] += 1
        if buffer_data['index'] == length:
            buffer_data['index'] = 0
    else:
        text = 'Ой, соре, {}, буффер-то пустой!'.format(user_name)

    file = open('Buffers_2\\{}.txt'.format(buffer_name), mode='w', encoding='UTF-8')
    json.dump(buffer_data, file)
    file.close()
    return text, attachments


# -----===== GET MEDIA FROM BUFFER =====-----
def copy_from_buffer(buffer_name, media_number, attachments, user_name):
    file = open('Buffers_2\\{}.txt'.format(buffer_name), mode='r', encoding='UTF-8')
    buffer_data = json.load(file)
    file.close()

    if len(buffer_data['media_list']) > 0:
        try:
            if media_number <= 0:
                raise IndexError
            if buffer_data['media_type']:
                text = 'Ваш текст:\n\n' + buffer_data['media_list'][media_number - 1]
            else:
                attachments.append(buffer_data['media_list'][media_number - 1])
                text = 'Ваше вложение, {}'.format(user_name)
        except IndexError:
            text = 'А попробуй другой номер вложения x_x'
    else:
        text = 'Ой, соре, {}, буффер-то пустой!'.format(user_name)

    file = open('Buffers_2\\{}.txt'.format(buffer_name), mode='w', encoding='UTF-8')
    json.dump(buffer_data, file)
    file.close()
    return text, attachments


# -----===== GET MEDIA FROM BUFFER =====-----
def random_from_buffer(buffer_name, attachments, user_name):
    file = open('Buffers_2\\{}.txt'.format(buffer_name), mode='r', encoding='UTF-8')
    buffer_data = json.load(file)
    file.close()

    length = len(buffer_data['media_list'])
    if length > 0:
        if buffer_data['media_type'] == 'text':
            text = 'Ваш текст:\n\n' + buffer_data['media_list'][random.randint(0, length - 1)]
        else:
            attachments.append(buffer_data['media_list'][random.randint(0, length - 1)])
            text = 'Ваше вложение, {}'.format(user_name)
    else:
        text = 'Ой, соре, {}, буффер-то пустой!'.format(user_name)

    file = open('Buffers_2\\{}.txt'.format(buffer_name), mode='w', encoding='UTF-8')
    json.dump(buffer_data, file)
    file.close()
    return text, attachments


# -----===== REMOVE ALL USERS FROM BUFFER =====-----
def remove_users(buffer_name):
    list_dir = os.listdir('Users_2')
    for user_file in list_dir:
        if int(user_file[:-4]) > 0:
            file = open('Users_2\\{}'.format(user_file), mode='r', encoding='utf-8')
            user_data = json.load(file)
            file.close()

            try:
                user_data['buffers'].remove(buffer_name)
                Log.update_user(user_data)
            except ValueError:
                pass


# -----===== CHANGE PASSWORD TO BUFFER AND KICK ALL USERS =====-----
def change_buffer_password(data):
    text = data['text'].split()
    buffer_name = text[2]
    new_password = text[3]

    file = open('Buffers_2\\{}.txt'.format(buffer_name), mode='r', encoding='UTF-8')
    buffer_data = json.load(file)
    file.close()

    buffer_data['password'] = new_password

    file = open('Buffers_2\\{}.txt'.format(buffer_name), mode='w', encoding='UTF-8')
    json.dump(buffer_data, file)
    file.close()

    remove_users(buffer_name)
    add_user_to_buffer(data['user'], buffer_name, new_password)

    return 'Дело сделано...'


# -----===== DELETE BUFFER =====-----
def delete_buffer(buffer_name):
    remove_users(buffer_name)
    os.remove('Buffers_2\\{}.txt'.format(buffer_name))
    return 'Ну вот и всё... Мы потеряли эту инфу :/'


# -----===== SHOWS INFO ABOUT BUFFER =====-----
def buffer_info(buffer_name):
    file = open('Buffers_2\\{}.txt'.format(buffer_name), mode='r', encoding='UTF-8')
    buffer_data = json.load(file)
    file.close()

    return 'Буффер: {}\n' \
           'Тип медиа-файлов: {}\n' \
           'Кол-во медиа-файлов: {}'.format(buffer_name, buffer_data['media_type'], len(buffer_data['media_list']))


allowed_media = ['photo', 'audio', 'video', 'doc', 'all', 'text']
