import os
import json

path = 'Users_2'

list_name = os.listdir(path)
quests = {}
for name in os.listdir('Quests'):
    quests.update({name: {'allowed': True,
                          'completed': False,
                          }
                   })
for user_file in list_name:
    file = open('{}\\{}'.format(path, user_file), mode='r')
    json_data = json.load(file)
    file.close()
    data = {"user_id": json_data['user_id'],
            "user_name": json_data['user_name'],
            "status": json_data['status'],
            "mute": json_data['mute'],
            "is_quest": json_data['is_quest'],
            "quest": {"cur_quest": json_data['quest']['cur_quest'],
                      "cur_stage": json_data['quest']['cur_stage'],
                      "variables": [],
                      "booleans": [],
                      "quests": quests,
                      },
            "buffers": [],
            }
    file = open('{}\\{}'.format(path, user_file), mode='w')
    json.dump(data, file)
    file.close()
print('Done!')
