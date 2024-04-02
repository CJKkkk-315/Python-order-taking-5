import socket
import json
import requests
def request_to_json(msg):
    for i in range(len(msg)):
        if msg[i]=="{" and msg[-1]=="\n":
            return json.loads(msg[i:])
    return None
def get_build_list():
    return

    # res = requests.get('http://127.0.0.1:5700/get_guild_member_list?guild_id=647583073978243001')
    # print(res.text)
    # import requests
    #
    # api_url = 'http://127.0.0.1:5700/send_private_msg'
    # user_id = 1121033787  # 目标用户的 QQ 号
    # image_url = 'https://gchat.qpic.cn/qmeetpic/608459523976235368/635713599-2716999926-28C934029E09224548C98D780FCB4B38/0?term=255'
    #
    # data = {
    #     'user_id': user_id,
    #     'message': f'[CQ:image,file={image_url}]'
    # }
    #
    # response = requests.post(api_url, json=data)
    # print(response.text)


get_build_list()