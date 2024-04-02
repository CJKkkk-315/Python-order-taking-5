import socket
import pyautogui
def send():
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')
    send_img('file:///E:/PYTHON接单5/流浪商人机器人/screenshot.png')


import requests

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
def send_img(img_url):
    api_url = 'http://127.0.0.1:5700/send_group_msg'
    group_id = 928896763
    image_url = img_url
    data = {
        'group_id': group_id,
        'message': f'[CQ:image,file={image_url}]'
    }
    response = requests.post(api_url, json=data)
    print(response.text)

import keyboard

def trigger_function():
    send()

# 定义一个监听器，当检测到 Alt + Shift + M 被同时按下时，执行 trigger_function
keyboard.add_hotkey('alt+shift+m', trigger_function)

print("Press Alt + Shift + M to trigger the function. Press ESC to exit.")

# 开始监听按键事件
keyboard.wait('esc')

# 当按下 ESC 时，程序将结束。

