import random
import timeit

import numpy as np

import Functions


class Specimen:
    def __init__(self, matrix):
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
                permutation = list(Functions.sums(self.size, rows[row]))
                rows_ = Functions.filter(permutation, temp_columns, row)
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
        return np.count_nonzero(self.matrix == 0) - self.size

    def display(self):
        print(self.matrix, "\n")


class Population(Specimen):
    def __init__(self, size):
        self.specimens = []
        self.elite = None
        self.size = size

    def make_population(self, matrix):
        for i in range(self.size):
            S = Specimen(matrix)
            S.initialize_matrix_change()
            self.specimens.append(S)

    def mutation(self):
        random_specimen = random.choice(self.specimens)
        self.specimens.remove(random_specimen)
        random_specimen = random_specimen.matrix

        a = 0
        b = len(random_specimen)
        c = len(random_specimen[0])

        row_1, row_2 = random.sample([i for i in range(a, b)], k=2)
        col_1, col_2 = random.sample([i for i in range(a, c) if i not in [row_1, row_2]], k=2)

        temp_matrix = [[random_specimen[col_1][row_1], random_specimen[col_2][row_1]],
                       [random_specimen[col_1][row_2], random_specimen[col_2][row_2]]]

        sum_row1 = random_specimen[col_1][row_1] + random_specimen[col_2][row_1]
        sum_row2 = random_specimen[col_1][row_2] + random_specimen[col_2][row_2]
        sum_col1 = random_specimen[col_1][row_1] + random_specimen[col_1][row_2]
        sum_col2 = random_specimen[col_2][row_1] + random_specimen[col_2][row_2]

        temp_matrix = Functions.change_matrix(temp_matrix, [sum_col1, sum_col2], [sum_row1, sum_row2])

        random_specimen[col_1][row_1] = temp_matrix[0][0]
        random_specimen[col_2][row_1] = temp_matrix[0][1]
        random_specimen[col_1][row_2] = temp_matrix[1][0]
        random_specimen[col_2][row_2] = temp_matrix[1][1]

        self.specimens.append(Specimen(random_specimen))

    def crossover(self):
        parent1 = random.choice(self.specimens)
        self.specimens.remove(parent1)
        parent2 = random.choice(self.specimens)
        self.specimens.remove(parent2)

        parent1 = parent1.matrix
        parent2 = parent2.matrix
        DIV = (parent1 + parent2) // 2
        REM = (parent1 + parent2) % 2
        sum_row = []
        sum = 0
        for i in range(len(REM)):
            for j in range(len(REM[0])):
                sum += REM[i][j]
            sum_row.append(sum / 2)
            sum = 0

        sum_col = []
        sum = 0
        for i in range(len(REM)):
            for j in range(len(REM[0])):
                sum += REM[j][i]
            sum_col.append(sum / 2)
            sum = 0
        REM1, REM2 = Functions.ones(REM)

        self.specimens.append(Specimen(DIV + REM1))
        self.specimens.append(Specimen(DIV + REM2))

    def roulette_selection(self):
        qualities = []
        probabilities = {}
        qualtities_sum = 0
        population = []

        for i in range(self.size):
            qualities.append(self.specimens[i].quality())
            qualtities_sum += (self.specimens[i].quality())

        probabilities[0] = [0, np.ceil(qualities[0] / qualtities_sum * 100)]
        for i in range(1, self.size):
            probabilities[i] = [probabilities[i - 1][1],
                                probabilities[i - 1][1] + np.ceil(qualities[i] / qualtities_sum * 100)]
        for j in range(self.size):
            rand = np.random.randint(0, probabilities[self.size - 1][1])
            for i in range(self.size):
                if (probabilities[i][0] <= rand) and (probabilities[i][1] >= rand):
                    population.append(self.specimens[i])
                    break
        self.specimens = population

    def ranking_selection(self):
        qualities = []
        qualtities_sum = 0
        population = []
        for i in range(self.size):
            qualities.append(self.specimens[i].quality())
            qualtities_sum += (self.specimens[i].quality())
        q2 = qualities[:]
        q2.sort()
        r = int(0.75 * len(qualities))
        q = q2[-r:][::-1]
        i = 0
        while len(population) < self.size:
            for j in range(self.size - 1):
                if qualities[j] == q[i]:
                    population.append(self.specimens[j])
                    break
            i += 1
            if i == len(q) - 1:
                i = 0
        self.specimens = population

    def tournament_selection(self):
        count_groups = self.size // 3
        if count_groups - self.size / 3 != 0:
            count_groups += 1
        groups = [[] for i in range(count_groups)]

        g = 0
        i = 0
        while True:
            if i + 2 < self.size:
                groups[g].append(self.specimens[i])
                groups[g].append(self.specimens[i + 1])
                groups[g].append(self.specimens[i + 2])
                groups[g].sort(reverse=True, key=lambda s: s.quality())
            elif i + 1 < self.size:
                groups[g].append(self.specimens[i])
                groups[g].append(self.specimens[i + 1])
            elif i < self.size:
                groups[g].append(self.specimens[i])
            else:
                break
            i += 3
            g += 1

        population = []
        g = 0
        while len(population) < self.size:
            population.append(groups[g][0])
            g += 1
            if g == count_groups:
                g = 0
        self.specimens = population

    def best_specimen(self):
        qualities = []

        for i in range(self.size):
            qualities.append(self.specimens[i].quality())

        max_value = max(qualities)
        max_index = qualities.index(max_value)
        return self.specimens[max_index]

    def add_best_specimen_to_elite(self, best_specimen):
        self.elite = best_specimen

    def display_population(self):
        for specimen in self.specimens:
            specimen.display()


def ea(iterations, size_of_population, time, primitive_specimen):
    time_ea = 0
    population = Population(size=size_of_population)
    population.make_population(primitive_specimen)
    best_specimen_ = population.specimens[0]
    quality = best_specimen_.quality()
    i = 1
    while i <= iterations:
        [population.mutation() for i in range(10)]
        # [population.crossover() for i in range(10)]
        population.ranking_selection()

        if quality < best_specimen_.quality() or i == 1:
            print("iteration {0} - quality:\t".format(i), best_specimen_.quality())
            quality = best_specimen_.quality()

        if population.best_specimen().quality() > best_specimen_.quality():
            best_specimen_ = population.best_specimen()

        time_ea += timeit.timeit()
        if time_ea >= time:
            break
        i += 1

    return best_specimen_
