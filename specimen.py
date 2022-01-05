import random

import numpy as np

import functions


class Specimen:
    def __init__(self, matrix: np.ndarray):
        self.number_of_rows = matrix.shape[0]
        self.number_of_cols = matrix.shape[1]
        self.rows = np.sum(matrix, axis=1)
        self.cols = np.sum(matrix, axis=0)
        self.matrix = matrix

    def initialize_matrix_change(self):
        first_loop = True
        # self.matrix - (np.ones_like(self.matrix) - np.eye(self.number_of_rows, self.number_of_cols)).astype('uint8')
        while np.sum(self.matrix.diagonal()) != 0 or first_loop:
            visit = [(row, col) for row in range(self.number_of_rows) for col in range(self.number_of_cols)]
            # rows = [row - (self.number_of_rows - 1) for row in self.rows]
            # cols = [col - (self.number_of_cols - 1) for col in self.cols]
            rows = self.rows.copy()
            cols = self.cols.copy()
            matrix = np.zeros_like(self.matrix)
            while visit:
                row, col = random.choice(visit)
                val = min(rows[row], cols[col])
                matrix[row][col] = val
                rows[row] -= val
                cols[col] -= val
                visit.remove((row, col))
            # self.matrix = matrix + (
            #             np.ones_like(self.matrix) - np.eye(self.number_of_rows, self.number_of_cols)).astype('uint8')
            self.matrix = functions.reshape_initial_problem(matrix)
            first_loop = False

    def initialize_matrix_change2(self):
        first_loop = True
        matrix_ = np.zeros((len(self.matrix), len(self.matrix[0])), int)
        np.fill_diagonal(matrix_, 1)

        while np.sum(matrix_.diagonal()) != 0 or first_loop:
            visit1 = [(row, col) for row in range(self.number_of_rows) for col in range(self.number_of_cols)]
            visit2 = [(row, col) for row in range(self.number_of_rows) for col in range(self.number_of_cols)]
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

    def initialize_matrix_permutation(self):
        cols, rows = self.cols, self.rows
        matrix = np.zeros_like(self.matrix)
        while list(np.sum(matrix, axis=0)) != list(cols):
            temp_columns = cols
            for row in range(self.number_of_rows - 1):
                permutation = list(functions.sums(self.number_of_cols, rows[row]))
                rows_ = functions.filter(permutation, temp_columns, row)
                if len(rows_) == 0:
                    continue
                idx_random_row = np.random.randint(len(rows_))
                matrix[row] = rows_[idx_random_row]
                temp_columns = [temp_columns[i] - matrix[row][i] for i in range(self.number_of_cols)]
            if temp_columns[-1] != 0:
                continue
            matrix[-1] = temp_columns
        self.matrix = matrix

    def quality(self):
        return np.count_nonzero(self.matrix == 0)

    def display(self):
        print(self.matrix, "\n")
