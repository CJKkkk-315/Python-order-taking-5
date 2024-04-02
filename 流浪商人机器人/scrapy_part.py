import requests
import json

import datetime

import datetime

def previous_specific_hour_timestamp():
    # 定义指定的小时列表
    specific_hours = [22, 16, 10, 4]

    # 获取当前时间
    now = datetime.datetime.now()

    # 查找上一个指定整点
    prev_hour = next((hour for hour in specific_hours if hour <= now.hour), specific_hours[0])

    # 如果上一个指定整点是昨天的某个时间点
    if prev_hour > now.hour:
        prev_time = datetime.datetime(now.year, now.month, now.day - 1, prev_hour)
    else:
        prev_time = datetime.datetime(now.year, now.month, now.day, prev_hour)

    # 返回时间戳
    return prev_time.timestamp()




def get_now_statu():
    final_res = ""
    gift = json.load(open('gift.json', encoding='utf8'))
    gold_map = {}
    for g in gift['data']['list']:
        gold_map[g['id']] = [g['name'], g['rarity']]


    card = json.load(open('card.json', encoding='utf8'))
    card_map = {}
    for g in card['data']['list']:
        card_map[g['id']] = [g['name'], g['rarity']]

    serveri = json.load(open('severmap.json', encoding='utf8'))
    sever_map = {}
    for s in serveri['data']:
        sever_map[s['id']] = s['name']
    headers = {
      'x-ajax': '1'
    }
    target_time = str(int(previous_specific_hour_timestamp()))
    # target_time = '1704700800'
    for sever_id in [3,4,5,6,7,12,13,14,15,16,17]:
        final_res += f'{sever_map[str(sever_id)]}:\n'
        active = requests.get(f'https://emrpg.com/plugin.php?displayAt={target_time}&fromServer=lostarkcn&serverId={sever_id}&uri=merchants/active&id=tj_emrpg', headers=headers)
        active = json.loads(active.text)
        print(active)
        gifts_res = []
        cards_res = []
        gold_gift_n = 0
        if not active['data']:
            final_res += '未提交\n\n'
            continue
        for seller in active['data']:
            gifts = seller['rapportId'].split(',')
            for gift in gifts:
                if gold_map[gift][1] == 'Legendary':
                    gold_gift_n += 1
                gifts_res.append(gold_map[gift][0])
        gold_card_n = 0
        for seller in active['data']:
            cards = seller['cardId'].split(',')
            for card in cards:
                if card_map[card][1] == 'Legendary':
                    gold_card_n += 1
                cards_res.append(card_map[card][0])


        a = f'好感度: {",".join(gifts_res)}'
        b = f'卡牌: {",".join(cards_res) }'
        c = f'金好感数量: {gold_gift_n}'
        d = f'金卡牌数量: {gold_card_n}'
        final_res += c + '\n\n' + d + '\n\n'
    return final_res[:-2]

def get_detail(sever_name):
    final_res = ""
    gift = json.load(open('gift.json', encoding='utf8'))
    gold_map = {}
    for g in gift['data']['list']:
        gold_map[g['id']] = [g['name'], g['rarity']]

    card = json.load(open('card.json', encoding='utf8'))
    card_map = {}
    for g in card['data']['list']:
        card_map[g['id']] = [g['name'], g['rarity']]

    serveri = json.load(open('severmap.json', encoding='utf8'))
    sever_map = {}
    for s in serveri['data']:
        sever_map[s['name']] = s['id']
    if sever_name not in sever_map:
        return ''
    sever_id = sever_map[sever_name]
    headers = {
        'x-ajax': '1'
    }
    target_time = str(int(previous_specific_hour_timestamp()))
    # target_time = '1704700800'
    active = requests.get(
        f'https://emrpg.com/plugin.php?displayAt={target_time}&fromServer=lostarkcn&serverId={sever_id}&uri=merchants/active&id=tj_emrpg',
        headers=headers)
    active = json.loads(active.text)
    # print(active)
    gifts_res = []
    cards_res = []
    gold_gift_n = 0
    if not active['data']:
        final_res += '未提交\n'
        return final_res
    for seller in active['data']:
        gifts = seller['rapportId'].split(',')
        for gift in gifts:
            if gold_map[gift][1] == 'Legendary':
                gold_gift_n += 1
            gifts_res.append(gold_map[gift][0])
    gold_card_n = 0
    for seller in active['data']:
        cards = seller['cardId'].split(',')
        for card in cards:
            if card_map[card][1] == 'Legendary':
                gold_card_n += 1
            cards_res.append(card_map[card][0])

    a = f'好感度: {",".join(gifts_res)}'
    b = f'卡牌: {",".join(cards_res)}'
    c = f'金好感数量: {gold_gift_n}'
    d = f'金卡牌数量: {gold_card_n}'
    final_res += a + '\n\n' + b + '\n\n'
    return final_res[:-2]
