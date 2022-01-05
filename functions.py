import copy
import random

import numpy as np


# Obliczenie wszystkich możliwych permutacji sumujących do granicy
def sums(length, total_sum):
    if length == 1:
        yield (total_sum,)
    else:
        for value in range(total_sum + 1):
            for permutation in sums(length - 1, total_sum - value):
                yield (value,) + permutation


# Usunięcie permutacji, które przekraczają sumę w kolumnach
def filter(permutation, columns, layer):
    pop_idx = []
    for idx_p in range(len(permutation)):
        if (np.array((permutation[idx_p])) > np.array(columns)).any() or permutation[idx_p][layer] != 0:
            pop_idx.append(idx_p)
    for idx in pop_idx[::-1]:
        permutation.pop(idx)
    return permutation


def change_matrix(matrix, columns_, rows_):
    matrix_copy = np.copy(matrix)
    rows = np.copy(rows_)
    columns = np.copy(columns_)
    m = len(matrix)
    n = len(matrix[0])
    visit = [0 for j in range(m * n)]
    for i in range(0, m * n):
        visit[i] = i
    while visit:
        q = random.choice(visit)
        row = (q // n)
        col = (q % n)
        # row = visit[q]//m
        # col = visit[q] % m
        val = min(rows[row], columns[col])
        matrix_copy[row][col] = val
        rows[row] = rows[row] - val
        columns[col] = columns[col] - val
        visit.remove(q)
        # visit[i], visit[q] = visit[q], visit[i]
    return matrix_copy


def valid_test(m1, m2):
    m1_cols = np.sum(m1, axis=0)
    m1_rows = np.sum(m1, axis=1)
    m2_cols = np.sum(m2, axis=0)
    m2_rows = np.sum(m2, axis=1)

    return (m1_cols == m2_cols).all() and (m1_rows == m2_rows).all()


def find_min(Z, case=1):
    x = 'r'
    y = Z.shape[0]
    idx = 0

    if case == 1:
        for i in range(Z.shape[0]):
            if np.count_nonzero(Z[i] != 0) < y and np.count_nonzero(Z[i] != 0) != 0:
                y = np.count_nonzero(Z[i] != 0)
                idx = i
        for i in range(Z.shape[0]):
            if np.count_nonzero(Z.T[i] != 0) < y and np.count_nonzero(Z.T[i] != 0) != 0:
                y = np.count_nonzero(Z.T[i] != 0)
                idx = i
                x = 'c'
    if case == 2:
        for i in range(Z.shape[0]):
            if np.count_nonzero(Z[i] != 0) <= y and np.count_nonzero(Z[i] != 0) != 0:
                y = np.count_nonzero(Z[i] != 0)
                idx = i
        for i in range(Z.shape[0]):
            if np.count_nonzero(Z.T[i] != 0) < y and np.count_nonzero(Z.T[i] != 0) != 0:
                y = np.count_nonzero(Z.T[i] != 0)
                idx = i
                x = 'c'
    if case == 3:
        for i in range(Z.shape[0]):
            if np.count_nonzero(Z[i] != 0) < y and np.count_nonzero(Z[i] != 0) != 0:
                y = np.count_nonzero(Z[i] != 0)
                idx = i
        for i in range(Z.shape[0]):
            if np.count_nonzero(Z.T[i] != 0) <= y and np.count_nonzero(Z.T[i] != 0) != 0:
                y = np.count_nonzero(Z.T[i] != 0)
                idx = i
                x = 'c'
    if case == 4:
        for i in range(Z.shape[0]):
            if np.count_nonzero(Z[i] != 0) <= y and np.count_nonzero(Z[i] != 0) != 0:
                y = np.count_nonzero(Z[i] != 0)
                idx = i
        for i in range(Z.shape[0]):
            if np.count_nonzero(Z.T[i] != 0) <= y and np.count_nonzero(Z.T[i] != 0) != 0:
                y = np.count_nonzero(Z.T[i] != 0)
                idx = i
                x = 'c'
    return x, idx


def ones(Z, case=1):
    Z1 = copy.deepcopy(Z)
    z1 = np.zeros(Z.shape)
    z2 = np.zeros(Z.shape)
    while np.count_nonzero(Z == 0) != Z.shape[0] ** 2:
        x = find_min(Z, case)[0]
        idx = find_min(Z, case)[1]
        if x == 'r':
            one = True
            for i in range(Z.shape[0]):
                if Z[idx][i] == 1:
                    z_1 = np.count_nonzero(z1[idx] != 0)
                    z_2 = np.count_nonzero(z2[idx] != 0)
                    if z_1 == z_2:
                        if one:
                            z1[idx][i] = 1
                            one = False
                            Z[idx][i] = 0
                        else:
                            z2[idx][i] = 1
                            one = True
                            Z[idx][i] = 0
                    elif z_1 < z_2:
                        z1[idx][i] = 1
                        one = False
                        Z[idx][i] = 0
                    else:
                        z2[idx][i] = 1
                        one = True
                        Z[idx][i] = 0
        else:
            one = True
            for i in range(Z.shape[0]):
                if Z[i][idx] == 1:
                    z_1 = np.count_nonzero(z1.T[idx] != 0)
                    z_2 = np.count_nonzero(z2.T[idx] != 0)
                    if z_1 == z_2:
                        if one:
                            z1[i][idx] = 1
                            one = False
                            Z[i][idx] = 0
                        else:
                            z2[i][idx] = 1
                            one = True
                            Z[i][idx] = 0
                    elif z_1 < z_2:
                        z1[i][idx] = 1
                        one = False
                        Z[i][idx] = 0
                    else:
                        z2[i][idx] = 1
                        one = True
                        Z[i][idx] = 0

    if valid_test(z1, z2):
        return z1, z2
    else:
        if case == 4:
            return Z, Z
        else:
            return ones(Z1, case + 1)


def initialize_primitive_specimen(size_of_specimen, max_generated_value):
    problem_matrix = np.random.randint(low=0, high=max_generated_value, size=(size_of_specimen, size_of_specimen))
    np.fill_diagonal(problem_matrix, 0)
    return problem_matrix


def generate_initial_matrix(max_generated_value, size_of_matrix, density_coefficient):
    dense_matrix = np.random.randint(low=0, high=max_generated_value, size=(size_of_matrix, size_of_matrix))
    np.fill_diagonal(dense_matrix, 0)
    return dense_matrix - dense_matrix * (dense_matrix > (density_coefficient / 100 * max_generated_value))


def reshape_initial_problem(matrix):
    number_of_rows, number_of_cols = matrix.shape
    size_ = number_of_cols - number_of_rows
    if size_ > 0:
        matrix = np.pad(matrix, [(0, size_), (0, 0)])
    elif size_ < 0:
        matrix = np.pad(matrix, [(0, 0), (0, -size_)])
    return matrix


def delete_unexpected_rows_cols(matrix):
    rows = np.sum(matrix, axis=1)
    cols = np.sum(matrix, axis=0)

    rows_to_delete = [i for i in range(len(rows)) if rows[i] == 0]
    cols_to_delete = [j for j in range(len(cols)) if cols[j] == 0]

    return np.delete(np.delete(matrix, rows_to_delete, 0), cols_to_delete, 1)
