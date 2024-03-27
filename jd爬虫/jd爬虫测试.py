import requests
import json
import csv
import time
rr = []
# 这里放商品id
pidi = input('请输入商品id：')
time_sleep = float(input('请输入间隔秒数：'))
pids = [pidi]
for pid in pids:
    for score in [3, 2, 1]:
        url = f'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&client=pc&clientVersion=1.0.0&productId={pid}&score={score}&sortType=5&page=1&pageSize=10&isShadowSku=0&fold=1&bbtf=&shield='
        res = requests.get(url)
        data = json.loads(res.text)
        max_page = data['maxPage']
        print(max_page)
        for i in range(max_page):
            # 这里设置间隔秒数
            time.sleep(time_sleep)
            url = f'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&client=pc&clientVersion=1.0.0&productId={pid}&score={score}&sortType=5&page={i}&pageSize=10&isShadowSku=0&fold=1&bbtf=&shield='
            res = requests.get(url)
            data = json.loads(res.text)
            comments = data['comments']
            print(len(comments))
            for c in comments:
                if c in rr:
                    print(c)
                rr.append([c['nickname'], c['content'], c['score']])


    with open(f'{pid}.csv', 'w', newline='', encoding='UTF8') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(rr)