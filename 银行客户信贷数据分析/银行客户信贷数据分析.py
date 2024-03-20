import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.neighbors import KNeighborsClassifier
warnings.filterwarnings('ignore')
data = pd.read_csv('企业信用评估.csv')


data['DAYS_EMPLOYED'] = data['DAYS_EMPLOYED'].replace(365243, 0)
data['DAYS_BIRTH'] = data['DAYS_BIRTH'].abs()
data['DAYS_EMPLOYED'] = data['DAYS_EMPLOYED'].abs()
data['DAYS_REGISTRATION'] = data['DAYS_REGISTRATION'].abs()
data['DAYS_ID_PUBLISH'] = data['DAYS_ID_PUBLISH'].abs()
data = data.drop([data.columns[0]], axis=1)
print(data.isnull().any())

# 设置画布的行数和列数
rows = 2  # 行数
cols = 7  # 列数

fig, axs = plt.subplots(rows, cols, figsize=(15, 10))
for i, column in enumerate(data.columns):
    row = i // cols
    col = i % cols
    sns.boxplot(y=data[column], ax=axs[row, col])
    axs[row, col].set_title(column)
plt.tight_layout()
plt.show()

column_name = 'CNT_CHILDREN'
record = {0: 0, 1: 0}
for _, j in data.iterrows():
    record[j['TARGET']] += j[column_name]

plt.bar([0, 1],[record[0], record[1]])
plt.show()