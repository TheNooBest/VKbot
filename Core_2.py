import vk_api
import sys
import Parser_2 as Parse
import Commands_2 as Cmd
import Logs_2 as Log
import Quest_sys as Qst
from vk_api.longpoll import VkLongPoll, VkEventType


def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


# ----- ALL WE NEED TO DO ----

file = open('LOG_IN_DATA.txt', mode="r")
data = [line.strip() for line in file]
file.close()

vk_session = vk_api.VkApi(data[0], data[1]) , app_id=int(data[2]), captcha_handler=captcha_handler)

try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)
    sys.exit()

vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

print('Bot activated!')

while True:
    try:
        for event in longpoll.listen():
            data = Parse.collect_data(event, vk)
            if event.type == VkEventType.MESSAGE_NEW:
                print(data)
                Log.log_it(data, vk)
                if data['user']['is_quest']:
                    if data['command']:
                        Qst.quest_commands_full[data['command']](vk, data)
                else:
                    if data['command']:
                        Cmd.command_base[data['command']](vk, data)
    except Exception as e:
        print('Error :0')
        print(e)
