import os
import json

path = 'Users_2'
quest = '1) Testing'
new_access = False

list_name = os.listdir(path)

for user_file in list_name:
    file = open('{}\\{}'.format(path, user_file), mode='r', encoding='utf-8')
    data = json.load(file)
    file.close()

    data['quest']['quests'][quest]['allowed'] = new_access

    file = open('{}\\{}'.format(path, user_file), mode='w', encoding='utf-8')
    json.dump(data, file)
    file.close()

print('Done!')
