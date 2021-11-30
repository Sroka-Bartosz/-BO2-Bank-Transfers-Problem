import random
import timeit
import time
import numpy as np

import Functions


class Specimen:
    def __init__(self, size):
        self.matrix = np.zeros((size, size))
        self.size = size

    def specimen_from_matrix(self, matrix):
        self.matrix = matrix

    def initialize_matrix(self, columns, rows):
        while list(np.sum(self.matrix, axis=0)) != columns:
            temp_columns = columns
            for row in range(self.size - 1):
                permutation = list(Functions.sums(self.size, rows[row]))
                rows_ = Functions.filter(permutation, temp_columns, row)
                if len(rows_) == 0:
                    continue
                idx_random_row = np.random.randint(len(rows_))
                self.matrix[row] = rows_[idx_random_row]
                temp_columns = [temp_columns[i] - self.matrix[row][i] for i in range(self.size)]
            if temp_columns[-1] != 0:
                continue
            self.matrix[-1] = temp_columns

    def quality(self):
        return np.count_nonzero(self.matrix == 0)

    def display(self):
        print(self.matrix, "\n")


class Population(Specimen):
    def __init__(self, columns, rows, size):
        super().__init__(size)
        self.specimens = []
        self.size = 20
        self.columns = columns
        self.rows = rows

    def make_population(self):
        for i in range(self.size):
            S = Specimen(len(self.columns))
            S.initialize_matrix(self.columns, self.rows)
            self.specimens.append(S)

    def mutation(self):
        random_specimen = random.choice(self.specimens)
        self.specimens.remove(random_specimen)
        random_specimen = random_specimen.matrix
        a = 0
        b = len(random_specimen)
        c = len(random_specimen[0])
        row_1, row_2 = random.sample([i for i in range(a, b)], k=2)
        col_1, col_2 = random.choices([i for i in range(0, c) if i not in [row_1, row_2]], k=2)

        temp_matrix = [[random_specimen[row_1][col_1], random_specimen[row_1][col_2]], [random_specimen[row_2][col_1],
                                                                                        random_specimen[row_2][col_2]]]
        sum_row1 = random_specimen[row_1][col_1] + random_specimen[row_1][col_2]
        sum_row2 = random_specimen[row_2][col_1] + random_specimen[row_2][col_2]
        sum_col1 = random_specimen[row_1][col_1] + random_specimen[row_2][col_1]
        sum_col2 = random_specimen[row_1][col_2] + random_specimen[row_2][col_2]
        temp_matrix = Functions.change_matrix(temp_matrix, [sum_col1, sum_col2], [sum_row1, sum_row2])
        random_specimen[row_1][col_1] = temp_matrix[0][0]
        random_specimen[row_1][col_2] = temp_matrix[0][1]
        random_specimen[row_2][col_1] = temp_matrix[1][0]
        random_specimen[row_2][col_2] = temp_matrix[1][1]
        new_specimen = Specimen(b)
        new_specimen.specimen_from_matrix(random_specimen)
        self.specimens.append(new_specimen)

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
        REM1 = Functions.separate(REM)
        REM2 = REM - REM1

        child1 = Specimen(len(REM))
        child2 = Specimen(len(REM))

        child1.specimen_from_matrix(DIV + REM1)
        child2.specimen_from_matrix(DIV + REM2)

        self.specimens.append(child1)
        self.specimens.append(child2)

    def selection(self):
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
            rand = np.random.randint(0, 100)
            for i in range(self.size):
                if (probabilities[i][0] <= rand) and (probabilities[i][1] >= rand):
                    population.append(self.specimens[i])
                    break
        self.specimens = population

    def best_specimen(self):
        qualities = []

        for i in range(self.size):
            qualities.append(self.specimens[i].quality())

        max_value = max(qualities)
        max_index = qualities.index(max_value)
        return self.specimens[max_index]

    def display_population(self):
        for specimen in self.specimens:
            specimen.display()


def ea(iterations, size_of_population, time, columns, rows):
    time_ea = 0
    population = Population(columns=columns, rows=rows, size=size_of_population)
    population.make_population()
    best_specimen = population.specimens[0]
    i = 1
    while i <= iterations:
        print("quality iteration {0}:\t".format(i), best_specimen.quality())
        population.mutation()
        population.crossover()
        population.selection()
        if population.best_specimen().quality() > best_specimen.quality():
            best_specimen = population.best_specimen()
        time_ea += timeit.timeit()
        if time_ea >= time:
            break
        i += 1
    return best_specimen
