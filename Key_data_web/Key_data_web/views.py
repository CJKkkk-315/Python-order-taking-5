# myapp/views.py
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import csv
import sqlite3
import time
import random

# 获取正确答案的函数
def get_correct_ans(request):
    db_file = 'key_data.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CorrectAnswer")  # 从CorrectAnswer表中获取所有数据
    rows = cursor.fetchall()
    cursor.execute("SELECT * FROM User")  # 从User表中获取所有数据
    users = cursor.fetchall()
    user_id = len(users) + 1  # 设置全局变量user_id为用户数量+1
    request.session['user_id'] = user_id
    sql = '''INSERT INTO User VALUES (?)'''
    cursor.executemany(sql, [[user_id]])
    conn.commit()
    cursor.close()
    conn.close()
    correct_ans = []
    for row in rows:
        correct_ans.append(row)
    # now_user_n = len(correct_ans)
    format_ans = [[{},{},{}] for _ in range(len(users))]  # 初始化格式化答案列表
    for i in correct_ans:
        format_ans[int(i[0])-1][int(i[1])-1][i[3]] = i[4]  # 将正确答案格式化

    return format_ans

# 初始化数据库表的函数
def init_table():
    db_file = 'key_data.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    # 创建CorrectAnswer表
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS CorrectAnswer (
        "User ID" INTEGER,
        "Web ID" INTEGER,
        "Web Info ID" INTEGER,
        "Name of Web Info" TEXT,
        "Value (Correct Answer)" TEXT
    )
    '''
    cursor.execute(create_table_query)

    # 创建User表
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS User (
        "User ID" INTEGER
    )
    '''
    cursor.execute(create_table_query)

    # 创建KeyInformation表
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS KeyInformation (
            "Current User ID" INTEGER,
            "Web ID" INTEGER,
            "Attack or not" BOOL,
            "User ID" INTEGER,
            "Event" TEXT,
            "Timestamp" FLOAT
        )
        '''
    cursor.execute(create_table_query)

    conn.commit()
    cursor.close()
    conn.close()

# 将文本文件转换为字典的函数
def txt2dic(file_path):
    data = [i for i in open(file_path).read().split('\n') if i]  # 读取文件并分割成行
    d = {}
    for i in data:
        d[i.split(':')[0]] = i.split(':')[1]  # 将每行的内容转换成字典项
    return d

# 随机选择下一个操作的函数
def random_select(request):
    # global attack_user_id, attack_ans, attack_web_id
    rep_dict = request.session['rep_dict']
    format_cor_ans = request.session['format_cor_ans']
    if sum([v for v in rep_dict.values()]) == 0:
        return 'finished'  # 如果rep_dict所有值的和为0，则返回'finished'
    while True:
        web_list = [key for key in rep_dict]
        next_web = web_list[random.randint(0, len(rep_dict)-1)]  # 随机选择一个web ID
        if rep_dict[next_web]:
            rep_dict[next_web] -= 1
            if next_web.split('_')[1] != 'rep':
                uid, wid = next_web.split('_')
                attack_user_id = uid
                attack_ans = format_cor_ans[int(uid)-1][int(wid)-1]
                attack_web_id = wid
                request.session['attack_user_id'] = attack_user_id
                request.session['attack_ans'] = attack_ans
                request.session['attack_web_id'] = attack_web_id
                if attack_ans:
                    return 'attack'  # 返回'attack'表示攻击模式
            else:
                return next_web  # 返回web ID

            if sum([v for v in rep_dict.values()]) == 0:
                return 'finished'

# 初始化所有数据的函数
def init_all(request):
    # global rep_time, rep_dict, w1_ans, w2_ans, w3_ans, attack_ans, attack_web_id, attack_user_id, res, format_cor_ans, all_name_map, user_id
    init_table()  # 初始化数据库表
    rep_time = 2
    request.session['rep_time'] = rep_time
    request.session['w1_ans'] = {}
    request.session['w2_ans'] = {}
    request.session['w3_ans'] = {}
    request.session['attack_ans'] = None
    request.session['attack_web_id'] = None
    request.session['attack_user_id'] = None
    request.session['res'] = []
    rep_dict = {'w1_rep':rep_time-1, 'w2_rep':rep_time-1, 'w3_rep':rep_time-1,}
    format_cor_ans = get_correct_ans(request)  # 获取格式化后的正确答案
    all_name_map = {1:d1, 2:d2, 3:d3}  # 将文件数据映射到相应变量
    request.session['format_cor_ans'] = format_cor_ans
    request.session['all_name_map'] = all_name_map
    m = 1
    n = 1
    # 设置rep_dict字典以追踪重复操作
    user_id = request.session['user_id']

    now_attack_n = 0
    if user_id > 1:
    # if True:
        for i in range(1, user_id):
            if user_id - i < 1:
                break
            if format_cor_ans[user_id - i - 1][0]:
                now_attack_n += 1
                rep_dict[f'{user_id - i}_{1}'] = m
                rep_dict[f'{user_id - i}_{2}'] = m
                rep_dict[f'{user_id - i}_{3}'] = m
            if now_attack_n == n:
                break
    request.session['rep_dict'] = rep_dict

d1 = txt2dic('ans1.txt')
d2 = txt2dic('ans2.txt')
d3 = txt2dic('ans3.txt')

def get_start_w1(request):
    # global count, w1_ans, w2_ans, w3_ans, user_id, res

    if request.method == 'POST':
        user_id = request.session['user_id']
        w1_ans = request.session['w1_ans']

        all_keys = []
        for i in d1:
            all_keys.append(i)
        for key in all_keys:
            if request.POST.get(key).replace(' ','') == '':
                return JsonResponse({'status': 'failure', 'message': 'Input must be non empty'})
            w1_ans[key] = request.POST.get(key)

        keypress_data = request.POST.get('keypress_data')  # 按键数据 JSON 字符串
        print(keypress_data)
        data = json.loads(keypress_data)
        for event in data:
            # 若非按键数据则跳过
            if 'key' not in event:
                continue
            # 将这条按键数据记录到res列表中，包括用户id，网页id， 是否攻击，攻击者id，按键事件以及时间。
            res = request.session['res']
            res.append([user_id, 1, False, '', event['key'] + ' ' + event['type'], event['time']])
            request.session['res'] = res
        # 跳转到第二个网页
        return JsonResponse({'status': 'redirect', 'url': '/start2/'})
    else:
        # 第一次进入时，调用初始化函数
        init_all(request)
    return render(request, 'w1.html')
def get_start_w2(request):
    # global count, w1_ans, w2_ans, w3_ans, user_id, res

    if request.method == 'POST':
        w2_ans = request.session['w2_ans']
        user_id = request.session['user_id']
        all_keys = []
        for i in d2:
            all_keys.append(i)

        for key in all_keys:
            if request.POST.get(key).replace(' ','') == '':
                return JsonResponse({'status': 'failure', 'message': 'Input must be non empty'})
            w2_ans[key] = request.POST.get(key)

        keypress_data = request.POST.get('keypress_data')
        data = json.loads(keypress_data)
        for event in data:
            if 'key' not in event:
                continue
            res = request.session['res']
            res.append([user_id, 3, False, '', event['key'] + ' ' + event['type'], event['time']])
            request.session['res'] = res

        return JsonResponse({'status': 'redirect', 'url': '/start3/'})

    return render(request, 'w2.html')
def get_start_w3(request):
    # global count, w1_ans, w2_ans, w3_ans, user_id, res
    if request.method == 'POST':
        w3_ans = request.session['w3_ans']
        user_id = request.session['user_id']
        all_keys = []
        for i in d3:
            all_keys.append(i)

        for key in all_keys:
            if request.POST.get(key).replace(' ','') == '':
                return JsonResponse({'status': 'failure', 'message': 'Input must be non empty'})
            w3_ans[key] = request.POST.get(key)

        keypress_data = request.POST.get('keypress_data')  # 按键数据 JSON 字符串
        data = json.loads(keypress_data)
        for event in data:
            if 'key' not in event:
                continue
            res = request.session['res']
            res.append([user_id, 3, False, '', event['key'] + ' ' + event['type'], event['time']])
            request.session['res'] = res
        # 3次网页正确答案输入完毕后，调用随机选择函数选择下一次要输入的网页并跳转
        next_web = random_select(request)
        return JsonResponse({'status': 'redirect', 'url': f'/{next_web}/'})
    return render(request, 'w3.html')
def w1_rep(request):
    # global count, w1_ans, w2_ans, w3_ans, user_id, res
    w1_ans = request.session['w1_ans']
    user_id = request.session['user_id']
    if request.method == 'POST':
        now_ans = {}
        all_keys = []
        for i in d1:
            all_keys.append(i)
        success_flag = True
        for key in all_keys:
            now_ans[key] = request.POST.get(key)
        for key in now_ans:
            if now_ans[key] != w1_ans[key]:
                print(key, now_ans[key] ,w1_ans[key])
                success_flag = False
                break
        if success_flag:
            keypress_data = request.POST.get('keypress_data')  # 按键数据 JSON 字符串
            data = json.loads(keypress_data)
            for event in data:
                if 'key' not in event:
                    continue
                res = request.session['res']
                res.append([user_id, 1, False, '', event['key'] + ' ' + event['type'], event['time']])
                request.session['res'] = res
            next_web = random_select(request)
            return JsonResponse({'status': 'redirect', 'url': f'/{next_web}/'})
        else:
            return JsonResponse({'status': 'failure', 'message': 'Entered incorrectly'})
    # 重复输入函数 返回自己的输入答案
    return render(request, 'w1_rep.html', {'w_ans':w1_ans})
def w2_rep(request):
    # global count, w1_ans, w2_ans, w3_ans, user_id, res
    w2_ans = request.session['w2_ans']
    user_id = request.session['user_id']
    if request.method == 'POST':

        now_ans = {}
        all_keys = []
        for i in d2:
            all_keys.append(i)
        success_flag = True
        for key in all_keys:
            now_ans[key] = request.POST.get(key)
        for key in now_ans:
            if now_ans[key] != w2_ans[key]:
                print(key, now_ans[key], w2_ans[key])
                success_flag = False
                break
        if success_flag:
            keypress_data = request.POST.get('keypress_data')  # 按键数据 JSON 字符串
            data = json.loads(keypress_data)
            for event in data:
                if 'key' not in event:
                    continue
                res = request.session['res']
                res.append([user_id, 2, False, '', event['key'] + ' ' +  event['type'], event['time']])
                request.session['res'] = res
            next_web = random_select(request)
            return JsonResponse({'status': 'redirect', 'url': f'/{next_web}/'})
        else:
            return JsonResponse({'status': 'failure', 'message': 'Entered incorrectly'})
    return render(request, 'w2_rep.html', {'w_ans':w2_ans})
def w3_rep(request):
    # global count, w1_ans, w2_ans, w3_ans, user_id, res
    w3_ans = request.session['w3_ans']
    user_id = request.session['user_id']
    if request.method == 'POST':
        now_ans = {}
        all_keys = []
        for i in d3:
            all_keys.append(i)
        success_flag = True
        for key in all_keys:
            now_ans[key] = request.POST.get(key)
        for key in now_ans:
            if now_ans[key] != w3_ans[key]:
                print(key, now_ans[key], w3_ans[key])
                success_flag = False
                break
        if success_flag:
            keypress_data = request.POST.get('keypress_data')  # 按键数据 JSON 字符串
            data = json.loads(keypress_data)
            for event in data:
                if 'key' not in event:
                    continue
                res = request.session['res']
                res.append([user_id, 3, False, '', event['key'] + ' ' + event['type'], event['time']])
                request.session['res'] = res
            next_web = random_select(request)
            return JsonResponse({'status': 'redirect', 'url': f'/{next_web}/'})
        else:
            return JsonResponse({'status': 'failure', 'message': 'Entered incorrectly'})
        # return JsonResponse({'status': 'redirect', 'url': '/w3_rep/'})

    return render(request, 'w3_rep.html', {'w_ans':w3_ans})
def w_attack(request):
    # global count, w1_ans, w2_ans, w3_ans, user_id, res
    attack_ans = request.session['attack_ans']
    attack_web_id = request.session['attack_web_id']
    attack_user_id = request.session['attack_user_id']
    user_id = request.session['user_id']
    if request.method == 'POST':
        now_ans = {}
        all_keys = []
        for i in attack_ans:
            all_keys.append(i)
        success_flag = True
        for key in all_keys:
            now_ans[key] = request.POST.get(key)
        for key in now_ans:
            if now_ans[key] != attack_ans[key]:
                print(key, now_ans[key], attack_ans[key])
                success_flag = False
                break
        if success_flag:
            keypress_data = request.POST.get('keypress_data')  # 按键数据 JSON 字符串
            data = json.loads(keypress_data)
            for event in data:
                if 'key' not in event:
                    continue
                res = request.session['res']
                res.append([user_id, attack_web_id, True, attack_user_id, event['key'] + ' ' + event['type'], event['time']])
                request.session['res'] = res
            next_web = random_select(request)
            return JsonResponse({'status': 'redirect', 'url': f'/{next_web}/'})
        else:
            return JsonResponse({'status': 'failure', 'message': 'Entered incorrectly'})
    # 攻击模型，根据当前网页id，返回对应网页html，并返回被攻击者的答案
    if attack_web_id == '1':
        return render(request, 'w1_attack.html', {'attack_ans':attack_ans,'attack_user_id':attack_user_id})
    elif attack_web_id == '2':
        return render(request, 'w2_attack.html', {'attack_ans':attack_ans,'attack_user_id':attack_user_id})
    elif attack_web_id == '3':
        return render(request, 'w3_attack.html', {'attack_ans': attack_ans, 'attack_user_id': attack_user_id})
def finished_web(request):
    for key, value in request.session.items():
        print(key, value)
    # 当所有输入都完成后，将数据写入数据库
    db_file = 'key_data.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    sql = '''INSERT INTO KeyInformation VALUES (?, ?, ?, ?, ?, ?)'''
    res = request.session['res']
    w1_ans = request.session['w1_ans']
    w2_ans = request.session['w2_ans']
    w3_ans = request.session['w3_ans']
    user_id = request.session['user_id']
    all_name_map = request.session['all_name_map']
    cursor.executemany(sql, res)
    conn.commit()
    correct_ans = []
    for key in w1_ans:
        correct_ans.append([user_id, 1, all_name_map['1'][key], key, w1_ans[key]])
    for key in w2_ans:
        correct_ans.append([user_id, 2, all_name_map['2'][key], key, w2_ans[key]])
    for key in w3_ans:
        correct_ans.append([user_id, 3, all_name_map['3'][key], key, w3_ans[key]])
    sql = '''INSERT INTO CorrectAnswer VALUES (?, ?, ?, ?, ?)'''
    cursor.executemany(sql, correct_ans)
    conn.commit()

    return HttpResponse('Finished!')