import csv
import os
files = os.listdir()
files = [i for i in files if i.endswith('rdf')]
d = {'化合物表达式':[], '反应时间':[],'反应温度':[], '反应条件':[],'产率':[],'试剂（命名）':[],'催化剂':[]}
now = ''
keep = False
for file in files:
    data = open(file,encoding='utf8').read().split('\n')
    for i in range(len(data)):
        row = data[i]
        print(row)
        if row == '$MOL':
            keep = True
        if keep:
            now += row + '\n'
        if row == 'M  END':
            keep = False
            d['化合物表达式'].append(now)
            now = ''
        if row == '$DTYPE ROOT:RXD(1):TIM':
            d['反应时间'].append(' '.join(data[i+1].split()[1:]))
        if row == '$DTYPE ROOT:RXD(1):T':
            d['反应温度'].append(' '.join(data[i+1].split()[1:]))
        if row == '$DTYPE ROOT:RXD(1):COND':
            d['反应条件'].append(' '.join(data[i+1].split()[1:]))
        if row == '$DTYPE ROOT:RXD(1):PRT':
            d['催化剂'].append(' '.join(data[i+1].split()[1:]))
        if row == '$DTYPE ROOT:RXD(1):YD':
            d['产率'].append(' '.join(data[i+1].split()[1:]))
        if row == '$DTYPE ROOT:RXD(1):RGT':
            d['试剂（命名）'].append(' '.join(data[i+1].split()[1:]))
max_length = max(len(column) for column in d.values())

for key in d:
    while len(d[key]) < max_length:
        d[key].append('')
with open('res.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['序号'] + list(d.keys()))
    writer.writerows(zip([i+1 for i in range(max_length)], *d.values()))