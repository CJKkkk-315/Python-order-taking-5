import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

#
# def read_ids(file_path):
#     """ Reads a file containing ids and returns a list of ids. """
#     with open(file_path, 'r', encoding='utf-8') as file:
#         ids = file.read().splitlines()
#     return ids
#
# def create_rating_matrix(data_file, user_ids):
#     """ Creates a 10000x10000 matrix based on the given data file. """
#     # Initialize a 10000x10000 matrix with zeros
#     rating_matrix = np.zeros((10000, 10000))
#
#     count = 0
#     with open(data_file, 'r') as file:
#         for line in file:
#             count += 1
#             user_id, movie_id, rating, _ = line.split()
#             # Convert ids to indices
#             user_index = user_ids[user_id]
#             # Update the matrix with the rating
#             rating_matrix[user_index][int(movie_id)-1] = int(rating)
#
#     return rating_matrix
#
#
# user_ids = {user_id: index for index, user_id in enumerate(read_ids('users.txt'))}
# train_matrix = create_rating_matrix('netflix_train.txt', user_ids)
# test_matrix = create_rating_matrix('netflix_test.txt', user_ids)
#
# print(type(train_matrix))
# print(type(test_matrix))
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix


def predict_ratings(train_matrix):
    # 将训练矩阵转换为稀疏矩阵格式
    train_sparse_matrix = csr_matrix(train_matrix)

    # 计算用户间的余弦相似度
    user_similarity = cosine_similarity(train_sparse_matrix)

    # 处理分母为0的情况
    user_similarity[np.isnan(user_similarity)] = 0

    # 计算每个用户的平均评分（只考虑非零评分）
    mean_user_rating = np.true_divide(train_matrix.sum(1), (train_matrix != 0).sum(1))

    # 预测评分
    pred_ratings = np.zeros(train_matrix.shape)
    for i in range(train_matrix.shape[0]):  # 遍历每个用户
        for j in range(train_matrix.shape[1]):  # 遍历每部电影
            # 使用相似用户的评分和相似度加权平均来预测评分
            sim_users = user_similarity[i]
            user_ratings = train_matrix[:, j]
            nonzero_indices = user_ratings > 0
            if np.sum(nonzero_indices) > 0:
                weighted_ratings = np.dot(sim_users[nonzero_indices], user_ratings[nonzero_indices])
                sum_sim = np.sum(np.abs(sim_users[nonzero_indices]))
                pred_rating = weighted_ratings / sum_sim
                pred_ratings[i, j] = pred_rating
            else:
                # 如果没有相似用户评分，则使用该用户的平均评分
                pred_ratings[i, j] = mean_user_rating[i]

    # 将预测评分四舍五入为整数，并确保评分在0到5之间
    pred_ratings = np.clip(np.rint(pred_ratings), 0, 5)
    return pred_ratings

import numpy as np

def generate_random_matrices(num_users, num_movies):
    # 生成随机训练矩阵和测试矩阵
    # 评分范围是0-5，其中0表示未评分
    # 使用较低的概率生成评分，以模拟稀疏的用户-电影矩阵
    train_matrix = np.random.choice([0, 1, 2, 3, 4, 5], size=(num_users, num_movies), p=[0.7, 0.07, 0.03, 0.03, 0.12, 0.05])
    test_matrix = np.random.choice([0, 1, 2, 3, 4, 5], size=(num_users, num_movies), p=[0.7, 0.07, 0.03, 0.03, 0.12, 0.05])

    return train_matrix, test_matrix

# 生成1000个用户和1000个电影的训练和测试矩阵
train_matrix, test_matrix = generate_random_matrices(1000, 1000)



predicted_ratings = predict_ratings(train_matrix, test_matrix)
print(predicted_ratings)
d = {}
for i in range(len(predicted_ratings)):
    for j in range(len(predicted_ratings[i])):
        d[predicted_ratings[i][j]] = d.get(predicted_ratings[i][j],0) + 1
print(d)
from sklearn.metrics import mean_squared_error
from math import sqrt

rmse = sqrt(mean_squared_error(test_matrix, predicted_ratings))

print(rmse)
exit(0)


def calculate_rmse(test_matrix, prediction_matrix):
    print(prediction_matrix)
    """ Calculate the Root Mean Square Error between the test matrix and the prediction matrix. """
    diff = test_matrix - prediction_matrix
    sq_diff = diff.power(2) if isinstance(diff, csr_matrix) else np.square(diff)
    mse = np.sum(sq_diff) / (test_matrix.count_nonzero() if isinstance(test_matrix, csr_matrix) else np.count_nonzero(test_matrix))
    rmse = np.sqrt(mse)
    return rmse

def user_based_collaborative_filtering(train_matrix, test_matrix):
    """ Perform user-based collaborative filtering and calculate RMSE on test data. """
    # Convert to csr format for efficient arithmetic operations
    train_matrix_csr = csr_matrix(train_matrix)

    # Calculate cosine similarity between users
    user_similarity = cosine_similarity(train_matrix_csr)

    # Predict ratings
    # This step can be optimized for large datasets, as it can be quite memory intensive
    mean_user_rating = train_matrix_csr.mean(axis=1)
    ratings_diff = (train_matrix_csr - mean_user_rating).toarray()
    pred = mean_user_rating + user_similarity.dot(ratings_diff) / np.array([np.abs(user_similarity).sum(axis=1)]).T

    # Calculate RMSE
    prediction_matrix = csr_matrix(pred)
    rmse = calculate_rmse(csr_matrix(test_matrix), prediction_matrix)

    return rmse

# Assuming train_matrix and test_matrix are the matrices you have
rmse = user_based_collaborative_filtering(train_matrix, test_matrix)
print(f"RMSE: {rmse}")


