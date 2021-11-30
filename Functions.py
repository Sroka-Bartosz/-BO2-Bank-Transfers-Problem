import numpy as np
import random


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
    visit = [0 for j in range(m*n)]
    for i in range(0, m*n):
        visit[i] = i
    while visit:
        q = random.choice(visit)
        row = (q//n)
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


def separate(matrix):
    array_nonzero = np.nonzero(matrix)
    nonzero_index = np.transpose(array_nonzero)
    matrix_copy = np.copy(matrix)
    rows = []
    sum = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            sum += matrix[i][j]
        rows.append(sum / 2)
        sum = 0

    cols = []
    sum = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            sum += matrix[j][i]
        cols.append(sum / 2)
        sum = 0
    m = len(matrix)
    n = len(matrix[0])
    REM1 = np.zeros((m, n))
    while len(nonzero_index) > 0:
        q = random.choice(nonzero_index)
        row = q[0]
        col = q[1]
        val = min(rows[q[0]], cols[q[1]])
        matrix_copy[row][col] = val
        rows[row] = rows[row] - val
        cols[col] = cols[col] - val
        nonzero_index = np.delete(nonzero_index, np.where(np.all(nonzero_index == q, axis=1)), axis=0)
    # print("matrix before\n", matrix)
    # print("matrix after\n", matrix_copy)
    return matrix_copy


def find_min(Z):
  x = 'r'
  y = Z.shape[0]
  idx = 0
  for i in range(Z.shape[0]):
    if np.count_nonzero(Z[i] != 0) < y and np.count_nonzero(Z[i] != 0) != 0:
      y = np.count_nonzero(Z[i] != 0)
      idx = i
  for i in range(Z.shape[0]):
    if np.count_nonzero(Z.T[i] != 0) < y and np.count_nonzero(Z.T[i] != 0) != 0:
      y = np.count_nonzero(Z.T[i] != 0)
      idx = i
      x = 'c'
  return x, idx


def ones(Z):
    z1 = np.zeros(Z.shape)
    z2 = np.zeros(Z.shape)
    while np.count_nonzero(Z == 0) != Z.shape[0]**2:
      x = find_min(Z)[0]
      idx = find_min(Z)[1]
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
    return z1, z2