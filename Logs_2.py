import os
import datetime
import json


# -----===== CREATE NEW FILES TO LOG =====-----
def new_log(data):
    file = open('Raw_logs_2\\' + str(data['peer_id']) + '.txt', mode="w", encoding='utf-8')
    addition = "Общение начато. Время: " + str(data['time']) + '\n'
    file.write(addition)
    file.close()

    file = open('Logs_2\\' + str(data['peer_id']) + '.txt', mode="w", encoding='utf-8')
    file.write(addition)
    file.close()


# -----===== WRITE SOME DATA TO LOGS ( + RAW) =====-----
def log_it(data, vk):
    if not os.path.isfile('Logs_2\\' + str(data['peer_id']) + '.txt'):
        new_log(data)

    file = open('Raw_logs_2\\' + str(data['peer_id']) + '.txt', mode="a", encoding='utf-8')
    addition = str(data) + '\n'
    file.write(addition)
    file.close()

    file = open('Logs_2\\' + str(data['peer_id']) + '.txt', mode="a", encoding='utf-8')
    value = datetime.datetime.fromtimestamp(data['time'])
    if data['from_chat']:
        addition = '\n[user_id, time, message_id]\n[' + \
                 str(data['user_id']) + ', ' + \
                 str(value) + ', ' + \
                 str(data['message_id']) + ']\n'
    else:
        addition = '\n[time, message_id]\n[' + \
                 str(value) + ', ' + \
                 str(data['message_id']) + ']\n'
    addition += data['user']['user_name'] + ':\n'
    if data['text']:
        addition += data['text'] + '\n'
    if data['attachments']:
        addition += str(data['attachments']) + '\n'
    if data['fwd_messages']:
        addition += add_forward(data['fwd_messages'], 1, vk)
    file.write(addition)
    file.close()


# -----===== CREATE NEW USER FILE =====-----
def new_user(vk, user_id):
    quest_arr = os.listdir("Quests")
    completed = []
    allowed = []
    for i in quest_arr:
        completed.append(False)
        allowed.append(True)
    allowed[0] = False
    file = open('Users_2\\' + str(user_id) + '.txt', mode="w", encoding='UTF-8')
    data = {"user_id": user_id,
            "user_name": vk.users.get(user_ids=user_id)[0]['first_name'],
            "status": 'standard',
            "mute": False,
            "is_quest": False,
            "quest": {"cur_quest": None,
                      "cur_stage": None,
                      "variables": [],
                      "booleans": [],
                      "allowed": allowed,
                      "completed": completed,
                      },
            "buffers": [],
            }
    json.dump(data, file)
    file.close()


# -----===== GET USER FILE WITH USER ID =====-----
def get_user(user_id):
    file = open('Users_2\\' + user_id + '.txt', mode="r", encoding='UTF-8')
    data = json.load(file)
    file.close()
    return data


# -----===== REWRITE USER FILE WITH NEW DATA =====-----
def update_user(user):
    file = open('Users_2\\{}.txt'.format(user['user_id']), mode='w', encoding='UTF-8')
    json.dump(user, file)
    file.close()


# -----===== ADD FORWARD MESSAGES TO LOG =====-----
def add_forward(fwd, count, vk):
    indent = '\t' * count
    string = ''
    for message in fwd:
        value = datetime.datetime.fromtimestamp(message['date'])
        if not os.path.isfile('Users_2\\' + str(message['from_id']) + '.txt'):
            new_user(vk, message['from_id'])
        user = get_user(str(message['from_id']))
        string += '\n' +\
                  indent + '[user_id, time]\n' + \
                  indent + '[' + str(message['from_id']) + ', ' + str(value) + ']\n' + \
                  indent + user['user_name'] + ':\n'
        if message['text']:
            string += indent + message['text'] + '\n'
        if message['attachments']:
            string += str(message['attachments']) + '\n'
        try:
            string += add_forward(message['fwd_messages'], count + 1, vk)
        except KeyError:
            pass
    return string
