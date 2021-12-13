import random

import numpy as np

import functions


class Specimen:
    def __init__(self, matrix: np.ndarray):
        self.size = matrix.shape[0]
        self.rows = np.sum(matrix, axis=1)
        self.cols = np.sum(matrix, axis=0)
        self.matrix = matrix

    def initialize_matrix_permutation(self):
        cols, rows = self.cols, self.rows
        matrix = np.zeros_like(self.matrix)
        while list(np.sum(matrix, axis=0)) != list(cols):
            temp_columns = cols
            for row in range(self.size - 1):
                permutation = list(functions.sums(self.size, rows[row]))
                rows_ = functions.filter(permutation, temp_columns, row)
                if len(rows_) == 0:
                    continue
                idx_random_row = np.random.randint(len(rows_))
                matrix[row] = rows_[idx_random_row]
                temp_columns = [temp_columns[i] - matrix[row][i] for i in range(self.size)]
            if temp_columns[-1] != 0:
                continue
            matrix[-1] = temp_columns
        self.matrix = matrix

    def initialize_matrix_change(self):
        first_loop = True
        matrix_ = np.zeros((len(self.matrix), len(self.matrix[0])), int)
        np.fill_diagonal(matrix_, 1)

        while np.sum(matrix_.diagonal()) != 0 or first_loop:
            visit1 = [(row, col) for row in range(self.size) for col in range(self.size)]
            visit2 = [(row, col) for row in range(self.size) for col in range(self.size)]
            rows, cols = self.rows.copy(), self.cols.copy()
            rows1 = []
            rows2 = []
            cols1 = []
            cols2 = []
            for x in rows:
                temp = x // 3
                rows1.append(x // 3)
                rows2.append((x - temp))
            for y in cols:
                temp = y // 3
                cols1.append(y // 3)
                cols2.append((y - temp))

            matrix1 = np.zeros_like(self.matrix)
            matrix2 = np.zeros_like(self.matrix)

            while visit1 and visit2:
                row1, col1 = random.choice(visit1)
                val1 = min(rows1[row1], cols1[col1])
                matrix1[row1][col1] = val1
                rows1[row1] = rows1[row1] - val1
                cols1[col1] = cols1[col1] - val1
                visit1.remove((row1, col1))

                row2, col2 = random.choice(visit2)
                val2 = min(rows2[row2], cols2[col2])
                matrix2[row2][col2] = val2
                rows2[row2] = rows2[row2] - val2
                cols2[col2] = cols2[col2] - val2
                visit2.remove((row2, col2))

            matrix_ = matrix1 + matrix2
            arr1, arr2 = np.nonzero(rows1)[0], np.nonzero(rows2)[0]
            arr3, arr4 = np.nonzero(cols1)[0], np.nonzero(cols2)[0]

            if len(arr1) == 0 and len(arr2) == 0 and len(arr3 == 0) and len(arr4[0]) == 0:
                continue
            else:
                if len(arr1) == 1 and len(arr3) == 1:
                    a1, b1 = int(arr1), int(arr3)
                    matrix_[a1][b1] = matrix_[a1][b1] + rows1[a1]
                if len(arr2) == 1 and len(arr3) == 1:
                    a1, b1 = int(arr2), int(arr3)
                    matrix_[a1][b1] = matrix_[a1][b1] + rows2[a1]
                if len(arr1) == 1 and len(arr4) == 1:
                    a1, b1 = int(arr1), int(arr4)
                    matrix_[a1][b1] = matrix_[a1][b1] + rows1[a1]
                if len(arr2) == 1 and len(arr4) == 1:
                    a1, b1 = int(arr2), int(arr4)
                    matrix_[a1][b1] = matrix_[a1][b1] + rows2[a1]

            first_loop = False
        self.matrix = matrix_

        # self.matrix = np.abs(np.ones_like(self.matrix) - np.eye(self.matrix.shape[0], self.matrix.shape[1]) - self.matrix)

    def quality(self):
        return np.count_nonzero(self.matrix == 0)

    def display(self):
        print(self.matrix.astype('uint8'), "\n")
