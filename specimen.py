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
        while np.sum(self.matrix.diagonal()) != 0:
            visit = [(row, col) for row in range(self.size) for col in range(self.size)]
            matrix = np.zeros_like(self.matrix)
            rows, cols = self.rows, self.cols
            while visit:
                row, col = random.choice(visit)
                val = min(rows[row], cols[col])
                matrix[row][col] = val
                rows[row] = rows[row] - val
                cols[col] = cols[col] - val
                visit.remove((row, col))
            self.matrix = matrix

    def quality(self):
        return np.count_nonzero(self.matrix == 0)

    def display(self):
        print(self.matrix, "\n")