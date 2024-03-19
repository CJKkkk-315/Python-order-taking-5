import numpy as np

def read_ids(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        ids = file.read().splitlines()
    return ids

def create_rating_matrix(data_file, user_ids):
    rating_matrix = np.zeros((10000, 10000))

    count = 0
    with open(data_file, 'r') as file:
        for line in file:
            count += 1
            user_id, movie_id, rating, _ = line.split()
            user_index = user_ids[user_id]
            rating_matrix[user_index][int(movie_id)-1] = int(rating)

    return rating_matrix


def matrix_factorization(X, alpha, lam, k, step):
    A = (X != 0).astype(int)
    U = np.random.rand(X.shape[0], k)
    V = np.random.rand(X.shape[1], k)
    for i in range(step):
        e = 0.5 * np.linalg.norm(A * (X - U @ V.T))**2 + lam*np.linalg.norm(U)**2 + lam*np.linalg.norm(V)**2
        print(e)
        Upd = (A * (U@V.T - X))@V + 2*lam*U
        Vpd = (A * (U@V.T - X))@U + 2*lam*V
        U -= alpha * Upd
        V -= alpha * Vpd
    return U@V.T
def generate_random_matrices(num_users, num_movies):
    train_matrix = np.random.choice([0, 1, 2, 3, 4, 5], size=(num_users, num_movies), p=[0.7, 0.07, 0.03, 0.03, 0.12, 0.05])
    test_matrix = np.random.choice([0, 1, 2, 3, 4, 5], size=(num_users, num_movies), p=[0.7, 0.07, 0.03, 0.03, 0.12, 0.05])

    return train_matrix, test_matrix
def get_rmse(test, pred):
    mask = (test != 0)
    diff = np.where(mask, test - pred, 0)
    mse = np.sum(diff ** 2) / np.sum(mask)
    rmse = np.sqrt(mse)
    return rmse

user_ids = {user_id: index for index, user_id in enumerate(read_ids('users.txt'))}
train_matrix = create_rating_matrix('netflix_train.txt', user_ids)
test_matrix = create_rating_matrix('netflix_test.txt', user_ids)

# train_matrix, test_matrix = generate_random_matrices(1000,1000)
pred_matrix = matrix_factorization(train_matrix, 1e-5, 0.01, 50, 100)
print(pred_matrix.shape)
print(test_matrix.shape)
print(get_rmse(test_matrix, pred_matrix))