from receive import rev_msg
import socket
from scrapy_part import get_now_statu, get_detail, previous_specific_hour_timestamp
import requests
import re
import json
from openai import OpenAI
client = OpenAI()

serveri = json.load(open('severmap.json', encoding='utf8'))
sever_map = {}
for s in serveri['data']:
    sever_map[s['name']] = s['id']
def send_img(img_url, sever_name):
    api_url = 'http://127.0.0.1:5700/send_group_msg'
    group_id = 928896763
    image_url = img_url
    data = {
        'group_id': group_id,
        'message': f'{sever_name} \n [CQ:image,file={image_url}]'
    }
    response = requests.post(api_url, json=data)
    print(response.text)
def send_img_group(img_url):
    api_url = 'http://127.0.0.1:5700/send_group_msg'
    group_id = 928896763
    image_url = img_url
    data = {
        'group_id': group_id,
        'message': f'[CQ:image,file={image_url}]'
    }
    response = requests.post(api_url, json=data)
    print(response.text)
def send_msg(resp_dict):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = '127.0.0.1'
    client.connect((ip, 5700))
    msg_type = resp_dict['msg_type']  # 回复类型（群聊/私聊）
    number = resp_dict['number']  # 回复账号（群号/好友号）
    msg = resp_dict['msg']  # 要回复的消息
    # 将字符中的特殊字符进行url编码
    msg = msg.replace(" ", "%20")
    msg = msg.replace("\n", "%0a")
    if msg_type == 'group':
        payload = "GET /send_group_msg?group_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    elif msg_type == 'private':
        payload = "GET /send_private_msg?user_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    print("发送" + payload)
    client.send(payload.encode("utf-8"))
    client.close()
    return 0
def gpt_answer(question):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你叫小土豆，你说话比较简短,没什么语气词"},
            {"role": "user", "content": f"{question}"}
        ]
    )
    return completion.choices[0].message.content
send_flag_text = False
send_flag_img = False
old_time = previous_specific_hour_timestamp()

while True:
    # print('send_flag_img', send_flag_img)
    # print('send_flag_text', send_flag_text)
    if previous_specific_hour_timestamp() != old_time:
        send_flag_text = False
        send_flag_img = False
    rev = rev_msg()
    # rev = {'post_type':'message', 'message_type':'guild','channel_id':'576607812','sender':{'nickname':'EMRPG'},'message':'[CQ:image,file=492e4f12d6b1c536d0595be3bc1cac5e.image,url=https://gchat.qpic.cn/qmeetpic/608459523976235368/635713599-2956077478-492E4F12D6B1C536D0595BE3BC1CAC5E/0?term=255]'}
    if rev and rev["post_type"] == "message":
        print(rev)
        if rev["message_type"] == "group": #群聊
            group = rev['group_id']
            if rev["raw_message"].startswith("[CQ:at,qq=1975373155] "):
                user_prompt = rev['raw_message'].replace('[CQ:at,qq=1975373155] ','')
                if user_prompt == '流浪商人':
                        msg = get_now_statu()
                        send_msg({'msg_type':'group','number':group,'msg':msg})
                elif '帮我骂他' in rev["raw_message"]:
                    if rev["raw_message"].count('CQ:at,qq') == 2:
                        target_qq = rev['raw_message'].split('CQ:at,qq=')[-1].split(']')[0]
                        send_msg({'msg_type': 'group', 'number': group, 'msg': f'[CQ:at,qq={target_qq}] 傻逼'})
                elif user_prompt in sever_map:
                    server_name = user_prompt
                    msg = get_detail(server_name)
                    if msg:
                        send_msg({'msg_type': 'group', 'number': group, 'msg': msg})
                else:
                    msg = gpt_answer(user_prompt)
                    send_msg({'msg_type': 'group', 'number': group, 'msg': msg})
        elif rev['message_type'] == 'guild': # 频道
            channel_map = {'576607812':'艾弗格雷斯', '576588274':'摩可可'}
            if rev['channel_id'] in channel_map:
                sever_name = channel_map[rev['channel_id']]
                data = json.load(open('guild_member.json', encoding='utf8'))
                guild_member_map = {}
                for m in data['data']['members']:
                    guild_member_map[m['tiny_id']] = m['role_name']
                if rev['sender']['tiny_id'] in guild_member_map:
                    print(1)
                    pattern = r"url=(https?://[^\]]+)"
                    match = re.search(pattern, rev['message'])
                    if match:
                        img_url = match.group(1)
                        send_img(img_url, sever_name)
                elif rev['sender']['nickname'] == 'EMRPG' or rev['sender']['nickname'] == '草履虫大王':
                    print(2)
                    pattern = r"url=(https?://[^\]]+)"
                    match = re.search(pattern, rev['message'])
                    if match:
                        img_url = match.group(1)
                        send_img(img_url, sever_name)
                elif '卡' in rev['message'] or '舔' in rev['message']:
                    if '吗' not in rev['message'] and '?' not in rev['message']:
                        send_msg({'msg_type': 'group', 'number': 928896763, 'msg': sever_name + '\n' + rev['message']})
                        send_flag_text = True
        else:
            continue
    else:  # rev["post_type"]=="meta_event":
        continue





