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
        self.matrix = self.matrix - (np.ones_like(self.matrix) - np.eye(self.number_of_rows, self.number_of_cols)).astype('uint8')
        self.update_rows_and_cols(self.matrix)
        while np.sum(self.matrix.diagonal()) != 0 or first_loop:
            visit = [(row, col) for row in range(self.number_of_rows) for col in range(self.number_of_cols)]
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
            self.matrix = matrix + (np.ones_like(self.matrix) - np.eye(self.number_of_rows, self.number_of_cols)).astype('uint8')
            first_loop = False
        self.update_rows_and_cols(self.matrix)
        self.matrix = functions.reshape_initial_problem(self.matrix)

    def update_rows_and_cols(self, matrix):
        self.rows = np.sum(matrix, axis=1)
        self.cols = np.sum(matrix, axis=0)

    def quality(self):
        return np.count_nonzero(self.matrix == 0)

    def display(self):
        print(self.matrix, "\n")
