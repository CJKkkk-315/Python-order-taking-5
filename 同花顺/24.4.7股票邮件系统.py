import ssl
import smtplib
from email.message import EmailMessage
import time
import tkinter as tk
import threading
import os
import tkinter.messagebox
import pyautogui
import pandas as pd


from pywinauto import Application



def send_email(EMAIL_ADDRESS,EMAIL_PASSWORD,receiver,title, stmp_id, port_id):
    context = ssl.create_default_context()
    sender = EMAIL_ADDRESS
    body = ''
    msg = EmailMessage()
    msg['subject'] = title
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content(body)
    with smtplib.SMTP_SSL(stmp_id, port_id, context=context) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def switch_focus_to_xiadan():
    # 连接到已经运行的Word实例
    app = Application(backend='uia').connect(path=r'D:\同花顺\xiadan.exe')
    # 获取窗口
    dlg = app.window(title='网上股票交易系统5.0')
    # 将焦点切换到窗口
    dlg.set_focus()

# 标记变量
stop_flag = 0
all_count = 0

def cycle_main():
    global stop_flag, all_count
    # key = 'jxcnynszlgnzhejh'
    # EMAIL_ADDRESS = '1121033787@qq.com'
    key = password_entry.get()
    EMAIL_ADDRESS = username_entry.get()
    receiver_content = content_text.get("1.0","end-1c")
    all_m = m_entry.get()
    stmp_id = stmp_entry.get()
    port_id = port_entry.get()
    receiver_info = {}
    print(receiver_content.split('\n'))
    for line in receiver_content.split('\n'):
        receiver_info[line.split()[0]] = line.split()[1].split(',')
    with open('SignalOut.txt') as f:
        old_records = f.read().split('\n')
        old_records = [i for i in old_records if i]
    while True:
        time.sleep(1)
        print("运行中...")
        if stop_flag:
            break
        with open('SignalOut.txt') as f:
            records = f.read().split('\n')
            records = [i for i in records if i]
        if len(records) > len(old_records):
            new_count = len(records) - len(old_records)
            new_records = records[-new_count:]
            print(new_records)
            switch_focus_to_xiadan()
            for r in new_records:
                sr = r.split('|')
                title = '|'.join(r.split('|')[1:5]) + ' ' + r.split('|')[-1] + '    ' + r.split('|')[-2]
                for u in receiver_info:
                    if sr[1] in receiver_info[u]:
                        send_email(EMAIL_ADDRESS,key,u,title,stmp_id,port_id)
                        all_count += 1

                pyautogui.press('f1')
                pyautogui.press('f2')

                pcode = sr[1]
                price = float(sr[-1])
                op = sr[3].replace(' ', '')
                pnumber = 0
                if '买入' in op:
                    if pcode not in buy_list:
                        continue
                    pnumber = int(int(all_m)/price)
                    pnumber -= pnumber%100
                    pyautogui.press('f1')
                elif '卖出' in op:
                    if pcode not in sell_map:
                        continue
                    pnumber = sell_map[pcode]
                    pyautogui.press('f2')
                    price -= 0.1
                price = round(price, 2)
                for i in range(10):
                    pyautogui.press('backspace')
                    time.sleep(0.1)
                pyautogui.typewrite(str(pcode))
                time.sleep(0.2)

                pyautogui.press('enter')
                for i in range(5):
                    pyautogui.press('backspace')
                    time.sleep(0.1)
                pyautogui.typewrite(str(price))

                pyautogui.press('enter')
                for i in range(10):
                    pyautogui.press('backspace')
                    time.sleep(0.1)
                pyautogui.typewrite(str(pnumber))

                time.sleep(0.2)
                pyautogui.press('enter')
                time.sleep(0.2)
                pyautogui.press('enter')
                time.sleep(0.2)
                pyautogui.press('enter')
                time.sleep(0.2)
                pyautogui.press('enter')
                time.sleep(0.2)
                pyautogui.press('enter')
                op_log_title = sr[1] + '|' + sr[2] + '|' + op + '|' + str(price) + '|' + sr[-2]
                for u in op_email_list:
                    send_email(EMAIL_ADDRESS, key, u, op_log_title)
                with open('OPlog.txt', 'a+') as f:
                    f.write(op_log_title + '\n')

        old_records = records
        root.update()





def start():
    state_now.config(text='启动中...')
    global stop_flag, all_count
    all_count = 0
    stop_flag = 0
    threading.Thread(target=cycle_main).start()

def stop():
    state_now.config(text='未启动')
    global stop_flag,all_count
    stop_flag = 1
    tkinter.messagebox.showinfo('执行完毕！',f'本次运行共发送{all_count}条邮件')

def save():
    f = open('config.txt','w')
    f.write(username_entry.get() + '\n')
    f.write(password_entry.get() + '\n')
    f.write(stmp_entry.get() + '\n')
    f.write(port_entry.get() + '\n')
    f.write(m_entry.get() + '\n')
    f.write(content_text.get("1.0", tk.END) + '\n')
    f.close()
    tkinter.messagebox.showinfo('结果','保存成功！')
if os.path.exists('config.txt'):
    content_data = open('config.txt').read()
    content_data = [i for i in content_data.split('\n') if i]
    EMAIL_ADDRESS = content_data[0]
    key = content_data[1]
    stmp_id = content_data[2]
    port_id = content_data[3]
    all_m = content_data[4]
    content_info = '\n'.join(content_data[5:])
else:
    key = ''
    EMAIL_ADDRESS = ''
    content_info = ''
    stmp_id = ''
    port_id = ''
    all_m = 0

if os.path.exists('OPconfig.xlsx'):
    opc = pd.read_excel('OPconfig.xlsx', header=None, dtype=str).values
    buy_list = [i for i in opc[0][1:] if str(i) != 'nan']
    sell_list = [i for i in opc[1][1:] if str(i) != 'nan']
    sell_map = {}
    for i in sell_list:
        sell_map[i.split('-')[0]] = int(i.split('-')[1])
    op_email_list = [i for i in opc[2][1:] if str(i) != 'nan']
else:
    buy_list = []
    sell_list = []
    op_email_list = []

print(all_m)
root = tk.Tk()

username_label = tk.Label(root, text="账号")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()
username_entry.insert(0,EMAIL_ADDRESS)

password_label = tk.Label(root, text="16位密钥")
password_label.pack()
password_entry = tk.Entry(root)
password_entry.pack()
password_entry.insert(0,key)

stmp_label = tk.Label(root, text="STMP")
stmp_label.pack()
stmp_entry = tk.Entry(root)
stmp_entry.pack()
stmp_entry.insert(0,stmp_id)

port_label = tk.Label(root, text="端口号")
port_label.pack()
port_entry = tk.Entry(root)
port_entry.pack()
port_entry.insert(0,port_id)

m_label = tk.Label(root, text="预设金额")
m_label.pack()
m_entry = tk.Entry(root)
m_entry.pack()
m_entry.insert(0,all_m)

content_label = tk.Label(root, text="内容")
content_label.pack()
content_text = tk.Text(root)
content_text.pack()
content_text.insert("1.0",content_info)
state_now = tk.Label(root, text='未启动')
state_now.pack()

start_button = tk.Button(root, text="启动", command=start)
start_button.pack()

stop_button = tk.Button(root, text="停止", command=stop)
stop_button.pack()

stop_button = tk.Button(root, text="保存", command=save)
stop_button.pack()

root.mainloop()
