import tkinter as tk
from threading import Thread, Event
import time
import pyautogui

# 声明全局变量
monitoring_thread = None
stop_event = Event()
codes = []

def check_file_changes(file_path, interval, callback, codes):
    last_content = ""
    while not stop_event.is_set():
        try:
            with open(file_path, 'r') as file:
                current_content = file.read()
                if current_content != last_content:
                    last_content = current_content
                    last_line = current_content.strip().split('\n')[-1]
                    stock_code = last_line.split('|')[1]
                    if stock_code in codes:
                        callback(stock_code)
        except Exception as e:
            print(f"Error reading file: {e}")
        time.sleep(interval)

def on_file_change(stock_code):
    if stock_code in codes:
        # 执行您的代码
        pyautogui.hotkey('alt', 'tab')
        pyautogui.press('f4')
        time.sleep(1)
        pyautogui.press('f1')
        pyautogui.press('backspace')
        time.sleep(1)
        pyautogui.press('backspace')
        pyautogui.press('backspace')
        pyautogui.press('backspace')
        time.sleep(1)
        pyautogui.press('backspace')
        pyautogui.press('backspace')

        file_path = 'D:\\SignalOut.txt'  # 更新为您的文件路径
        with open(file_path, 'r') as file:
            lines = file.readlines()
            last_line = lines[-1]

        stock_price = last_line.split('|')[-1].strip()
        stock_vol = round(50000 / float(stock_price), -2)
        pyautogui.typewrite(stock_code)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.typewrite(stock_price)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.typewrite(str(stock_vol))
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')

def start_monitoring():
    global monitoring_thread
    code_str = entry.get()
    if not code_str:
        tk.messagebox.showwarning("提示", "请输入股票代码")
        return
    codes.clear()
    codes.extend(code_str.split())
    print("Stock codes:", codes)

    if not monitoring_thread or not monitoring_thread.is_alive():
        stop_event.clear()
        monitoring_thread = Thread(target=check_file_changes, args=('SignalOut.txt', 1, on_file_change, codes))
        monitoring_thread.start()
        start_button.config(relief=tk.SUNKEN, bg='green')
    else:
        stop_monitoring()

def stop_monitoring():
    stop_event.set()
    start_button.config(relief=tk.RAISED, bg='red')

# 创建图形化界面
root = tk.Tk()
root.title("File Monitor")

entry = tk.Entry(root, width=50)
entry.pack()

start_button = tk.Button(root, text="Start Monitoring", command=start_monitoring)
start_button.pack()

root.mainloop()
