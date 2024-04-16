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
    xiadan_path = xiadan_entry.get()
    app = Application(backend='uia').connect(path=xiadan_path)
    # 获取窗口
    dlg = app.window(title='网上股票交易系统5.0')
    # 将焦点切换到窗口
    dlg.set_focus()

# 标记变量
stop_flag = 0
all_count = 0

def cycle_main():
    global stop_flag, all_count

    buy_list = [i for i in buy_entry.get().split() if i]
    sell_list = [i for i in sell_entry.get().split() if i]
    sell_map = {}
    for i in sell_list:
        sell_map[i.split('-')[0]] = int(i.split('-')[1])

    op_email_list = email_entry.get().split()
    check_flag = {}
    key = password_entry.get()
    EMAIL_ADDRESS = username_entry.get()
    # receiver_content = content_text.get("1.0","end-1c")
    all_m = m_entry.get()
    stmp_id = stmp_entry.get()
    port_id = port_entry.get()
    receiver_info = {}
    # print(receiver_content.split('\n'))
    # for line in receiver_content.split('\n'):
    #     receiver_info[line.split()[0]] = line.split()[1].split(',')
    with open('TdxSignal.txt') as f:
        old_records = f.read().split('\n')
        old_records = [i for i in old_records if i]
    while True:
        print(all_m)
        time.sleep(1)
        print("运行中...")
        if stop_flag:
            break
        with open('TdxSignal.txt') as f:
            records = f.read().split('\n')
            records = [i for i in records if i]
        if len(records) > len(old_records):
            new_count = len(records) - len(old_records)
            new_records = records[-new_count:]
            print(new_records)
            switch_focus_to_xiadan()
            for r in new_records:
                sr = r.split('|')

                pyautogui.press('f1')
                pyautogui.press('f2')

                pcode = sr[2]
                price = float(sr[6])
                flag = sr[4]
                op = sr[3].replace(' ', '')
                pnumber = 0
                if op == '1':
                    if pcode not in buy_list or (pcode, flag) in check_flag:
                        continue
                    pnumber = int(int(all_m)/price)
                    pnumber -= pnumber%100
                    check_flag[(pcode, flag)] = 1
                    pyautogui.press('f1')
                elif op == '-1':
                    if pcode not in sell_map or (pcode, flag) in check_flag:
                        continue
                    pnumber = sell_map[pcode]
                    check_flag[(pcode, flag)] = 1
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
                if op == '1':
                    op_log_title = pcode + '-' + sr[-1] + '-' + str(price) + '-' + str(pnumber) + '-' + '买入' + '-' + '已下单'
                elif op == '-1':
                    op_log_title = pcode + '-' + sr[-1] + '-' + str(price) + '-' + str(pnumber) + '-' + '卖出' + '-' + '已下单'
                else:
                    op_log_title = op + '操作未知'
                for u in op_email_list:
                    send_email(EMAIL_ADDRESS, key, u, op_log_title, stmp_id,port_id)
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

    f = open('opconfig.txt','w', encoding='utf8')
    f.write('发送邮箱：' + username_entry.get() + '\n')
    f.write('安全密码：' + password_entry.get() + '\n')
    f.write('服务地址：' + stmp_entry.get() + '\n')
    f.write('服务端口：' + port_entry.get() + '\n')
    f.write('买入金额：' + m_entry.get() + '\n')
    f.write('下单路径：' + xiadan_entry.get() + '\n')
    f.write('买入观察：' + buy_entry.get() + '\n')
    f.write('卖出观察：' + sell_entry.get() + '\n')
    f.write('推送邮件：' + email_entry.get() + '\n')
    # f.write(content_text.get("1.0", tk.END) + '\n')
    f.close()
    tkinter.messagebox.showinfo('结果','保存成功！')


if os.path.exists('opconfig.txt'):
    f = open('opconfig.txt',encoding='utf8')
    opc = f.read().split('\n')
    f.close()
    EMAIL_ADDRESS = opc[0].split('：')[1]
    key = opc[1].split('：')[1]
    stmp_id = opc[2].split('：')[1]
    port_id = opc[3].split('：')[1]
    all_m = opc[4].split('：')[1]
    xiadan_path = opc[5].split('：')[1]
    buy_content = opc[6].split('：')[1]
    sell_content = opc[7].split('：')[1]
    op_email_content = opc[8].split('：')[1]
else:
    EMAIL_ADDRESS = ''
    key = ''
    stmp_id = ''
    port_id = ''
    all_m = ''
    xiadan_path = ''
    buy_content = ''
    sell_content = ''
    op_email_content = ''

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

xiadan_label = tk.Label(root, text="下单路径")
xiadan_label.pack()
xiadan_entry = tk.Entry(root)
xiadan_entry.pack()
xiadan_entry.insert(0,xiadan_path)

buy_label = tk.Label(root, text="买入观察")
buy_label.pack()
buy_entry = tk.Entry(root, width=100)
buy_entry.pack()
buy_entry.insert(0,buy_content)

sell_label = tk.Label(root, text="卖出观察")
sell_label.pack()
sell_entry = tk.Entry(root, width=100)
sell_entry.pack()
sell_entry.insert(0,sell_content)

email_label = tk.Label(root, text="推送邮箱")
email_label.pack()
email_entry = tk.Entry(root, width=100)
email_entry.pack()
email_entry.insert(0,op_email_content)

# content_text.insert("1.0",content_info)
state_now = tk.Label(root, text='未启动')
state_now.pack()

start_button = tk.Button(root, text="启动", command=start)
start_button.pack()

stop_button = tk.Button(root, text="停止", command=stop)
stop_button.pack()

stop_button = tk.Button(root, text="保存", command=save)
stop_button.pack()

root.mainloop()
