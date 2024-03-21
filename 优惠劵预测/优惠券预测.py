# 引入所需的库
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score
from imblearn.under_sampling import RandomUnderSampler
import warnings
from sklearn.model_selection import GridSearchCV
warnings.filterwarnings('ignore')

# 定义一个函数用于数据预处理
def process_data(df, label_name):
    # 删除Coupon_id为空的行
    df = df[~df['Coupon_id'].isnull()]
    # 填充Distance列的空值为0
    df['Distance'] = df['Distance'].fillna(0)
    # 创建Label列，根据label_name列是否为空或者为空字符串来设置0或1
    df['Label'] = df[label_name].apply(lambda x: 0 if pd.isna(x) or x == '' else 1)
    # 将Discount_rate列拆分成x和y两列
    df[['x', 'y']] = df['Discount_rate'].str.split(':', expand=True)
    # 重新填充y列的空值为1
    df['y'] = df['y'].fillna(1)
    # 选择最终的列
    df = df[['Distance','x','y','Label']]
    return df

# 读取训练和测试数据
df1 = pd.read_csv('ccf_offline_stage1_train.csv')
df2 = pd.read_csv('ccf_offline_stage1_test_revised.csv')
# 对数据进行预处理
df1 = process_data(df1, 'Date')
df2 = process_data(df2, 'Date_received')
# 将处理后的训练和测试数据合并
df = pd.concat([df1,df2],axis=0)

# 分离特征和标签
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# 打印原始标签分布
class_counts = y.value_counts()
print(class_counts)

# 使用随机下采样方法来处理数据不平衡问题
rus = RandomUnderSampler()
X_res, y_res = rus.fit_resample(X, y)
# 打印下采样后的标签分布
class_counts = y_res.value_counts()
print(class_counts)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2)

# 定义一个字典来保存不同的分类模型
models = {
    "Decision Tree": DecisionTreeClassifier(),
    "Linear Regression": LogisticRegression(),
    "KNN": KNeighborsClassifier(),
    "SVM": SVC()
}

# 循环遍历字典中的每个模型
for name, model in models.items():
    # 训练模型
    model.fit(X_train, y_train)
    # 预测测试集
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    # 计算并打印各项评估指标
    acc = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)

    print(f"{name}:\n Accuracy: {acc:.2f}, Recall: {recall:.2f}, AUC: {auc:.2f}\n")

# 设置决策树模型的超参数搜索范围
param_grid = {
    'max_depth': [None, 10, 20, 30, 40, 50],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
# 初始化决策树模型
dt = DecisionTreeClassifier(random_state=0)
# 使用GridSearchCV进行超参数搜索
grid_search = GridSearchCV(dt, param_grid, cv=5, scoring='roc_auc')
grid_search.fit(X_train, y_train)

# 获取并打印最佳参数和分数
best_params = grid_search.best_params_
best_score = grid_search.best_score_
print("Best Parameters: ", best_params)
print("Best AUC: ", best_score)

# 使用最佳参数训练的模型
best_model = grid_search.best_estimator_

# 对最佳模型进行评估
y_pred = best_model.predict(X_test)
y_proba = best_model.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)

print(f"Best Decision Tree:\nAccuracy: {acc:.2f}, Recall: {recall:.2f}, AUC: {auc:.2f}\n")
