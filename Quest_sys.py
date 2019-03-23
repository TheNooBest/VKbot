from Logs_2 import update_user
from Commands_2 import send_message

divider = '<--->'


def get_text(text, user):
    try:
        index = text.index(divider)
        text = text[:index].split('#')
    except ValueError:
        pass

    for arg in text:
        if arg.startswith('bool'):
            arg = arg.split(' ', maxsplit=3)
            var_num = get_num_of_var(arg[0])
            check_for_var_count(var_num, user)
            if arg[1] == '==':
                if user['quest']['booleans'][var_num] == bool(arg[2]):
                    arg = arg[3]
                else:
                    arg = ''
            elif arg[1] == '!=':
                if user['quest']['booleans'][var_num] != bool(arg[2]):
                    arg = arg[3]
                else:
                    arg = ''
            else:
                arg = ''
        elif arg.startswith('var'):
            arg = arg.split(' ', maxsplit=3)
            var_num = get_num_of_var(arg[0])
            check_for_var_count(var_num, user)
            if arg[1] == '<':
                if user['quest']['variables'][var_num] < int(arg[2]):
                    arg = arg[3]
                else:
                    arg = ''
            elif arg[1] == '>':
                if user['quest']['variables'][var_num] > int(arg[2]):
                    arg = arg[3]
                else:
                    arg = ''
            elif arg[1] == '==':
                if user['quest']['variables'][var_num] == int(arg[2]):
                    arg = arg[3]
                else:
                    arg = ''
            else:
                arg = ''
        text += arg
    return text


def get_choose(text, user):
    choose_str = ''
    try:
        index = text.index(divider)
        choose_str = text[index + 5:].strip()
    except ValueError:
        pass

    choose_arr = []
    for line in choose_str:
        arg = line.split(' ')
        has_if = True
        accept = True
        while has_if:
            if arg[0].startswith('bool'):
                var_num = get_num_of_var(arg[0])
                check_for_bool_count(var_num, user)
                if arg[1] == '==':
                    if user['quest']['booleans'][var_num] == bool(arg[2]):
                        arg = arg[3:]
                    else:
                        accept = False
                elif arg[1] == '!=':
                    if user['quest']['booleans'][var_num] != bool(arg[2]):
                        arg = arg[3:]
                    else:
                        accept = False
                else:
                    accept = False
            elif arg[0].startswith('var'):
                var_num = get_num_of_var(arg[0])
                check_for_var_count(var_num, user)
                if arg[1] == '<':
                    if user['quest']['variables'][var_num] < int(arg[2]):
                        arg = arg[3:]
                    else:
                        accept = False
                elif arg[1] == '>':
                    if user['quest']['variables'][var_num] > int(arg[2]):
                        arg = arg[3:]
                    else:
                        accept = False
                elif arg[1] == '==':
                    if user['quest']['variables'][var_num] == int(arg[2]):
                        arg = arg[3:]
                    else:
                        accept = False
                else:
                    accept = False
            else:
                has_if = False
        if accept:
            choose_arr.append(arg)
    return choose_arr


def choose(vk, data):
    num = int(data['text'])
    user = data['user']
    path = 'Quests\\{}\\{}'.format(user['quest']['cur_quest'], user['quest']['cur_stage'])
    f = open(path, mode='r')
    text = f.read()
    f.close()

    choose_arr = get_choose(text, user)

    try:
        stage = choose_arr[num]
        if type(stage) is list:
            for arg in reversed(stage):
                if arg.startswith('bool'):
                    var_num = get_num_of_var(arg[:6])
                    if arg[6] == '+':
                        user['quest']['booleans'][var_num] = True
                    elif arg[6] == '-':
                        user['quest']['booleans'][var_num] = False
                    elif arg[6] == '!':
                        user['quest']['booleans'][var_num] = not user['quest']['booleans'][var_num]
                    else:
                        pass
                elif arg.startswith('var'):
                    var_num = get_num_of_var(arg[:5])
                    if arg[5] == '+':
                        user['quest']['variables'][var_num] += int(arg[6:])
                    elif arg[5] == '-':
                        user['quest']['variables'][var_num] -= int(arg[6:])
                    elif arg[5] == '=':
                        user['quest']['variables'][var_num] = int(arg[6:])
                    else:
                        pass
                elif arg.startswith('Open'):
                    new_quest = arg[5:]
                    user['quest']['quests'][new_quest]['allowed'] = True
                else:
                    stage = arg

        user['quest']['cur_stage'] = stage
        response = get_text(text, user)
        choose_arr = get_choose(text, user)
        stage = choose_arr[0]

        if stage == 'Completed':
            user['is_quest'] = False
            user['quest']['booleans'] = []
            user['quest']['variables'] = []
            user['quest']['quests'][user['quest']['cur_quest']]['completed'] = True
        else:
            user['quest']['cur_stage'] = stage
        update_user(user)

        new_data = {'peer_id': data['peer_id'],
                    'text': response,
                    'attachments': [],
                    'fwd_msg': '',
                    'user_id': data['user_id'],
                    }
        send_message(vk, new_data)
    except IndexError:
        pass


def leave(vk, data):
    user = data['user']
    user['is_quest'] = False
    user['quest']['booleans'] = []
    user['quest']['variables'] = []
    update_user(user)
    response = 'Наигрался, надеюсь :3'

    new_data = {'peer_id': data['peer_id'],
                'text': response,
                'attachments': [],
                'fwd_msg': '',
                'user_id': data['user_id'],
                }
    send_message(vk, new_data)


def help_me(vk, data):
    response = 'Тут всё просто\n'\
               + 'ПОМОЩЬ - вот это сообщение\n'\
               + 'ВЫХОД - Это, если тебе надоел квест :/\n'\
               + 'Потом ты можешь выбрать одну из предложенных циферок, чтобы выбрать соотв. вариант\n'

    new_data = {'peer_id': data['peer_id'],
                'text': response,
                'attachments': [],
                'fwd_msg': '',
                'user_id': data['user_id'],
                }
    send_message(vk, new_data)


# -----===== GET NUM OF VARIABLE =====-----
def get_num_of_var(text):
    text = text.split('_')
    return int(text[1])


def check_for_var_count(num, user):
    var_len = len(user['quest']['variables'])
    delta = num - var_len
    while delta > 0:
        delta -= 1
        user['quest']['variables'].append(0)
    update_user(user)


def check_for_bool_count(num, user):
    var_len = len(user['quest']['booleans'])
    delta = num - var_len
    while delta > 0:
        delta -= 1
        user['quest']['booleans'].append(False)
    update_user(user)


quest_commands = {'ПОМОЩЬ': help_me,
                  'ВЫЙТИ': leave,
                  }
quest_commands_full = {'ВЫБОР': choose,
                       }
quest_commands_full.update(quest_commands)
