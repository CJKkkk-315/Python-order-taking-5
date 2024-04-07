import time
import pyautogui
sr = '2023-05-12 10:16:25 : OrderMon信号|603505|金石资源|买入　|1-低吸|1Min|10:16:22|33.51'.split('|')

time.sleep(5)
all_m = 50000

pcode = sr[1]
price = float(sr[-1])
op = sr[3].replace(' ', '')
print(op, price, pcode)
if '买入' in op:
    pyautogui.press('f1')
elif '卖出' in op:
    pyautogui.press('f2')
for i in range(10):
    pyautogui.press('backspace')
    time.sleep(0.1)
pyautogui.typewrite(pcode)
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
pyautogui.typewrite(str(int(all_m / price)))

time.sleep(0.2)
pyautogui.press('enter')
time.sleep(0.2)
pyautogui.press('enter')