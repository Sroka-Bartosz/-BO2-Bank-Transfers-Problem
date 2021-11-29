import numpy as np

import Functions


class Specimen:
    def __init__(self, size):
        self.matrix = np.zeros((size, size))
        self.size = size

    def initialize_matrix(self, columns, rows):
        while list(np.sum(self.matrix, axis=0)) != columns:
            temp_columns = columns
            for row in range(self.size - 1):
                permutation = list(Functions.sums(self.size, rows[row]))
                rows_ = Functions.filter(permutation, temp_columns, row)
                idx_random_row = np.random.randint(len(rows_))
                self.matrix[row] = rows_[idx_random_row]
                temp_columns = [temp_columns[i] - self.matrix[row][i] for i in range(self.size)]
            if temp_columns[-1] != 0:
                continue
            self.matrix[-1] = temp_columns

    def quality(self):  # TO DO
        return np.count_nonzero(self.matrix == 0)

    def display(self):
        print(self.matrix)


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
        pass

    def crossover(self):
        pass

    def selection(self):
        qualities = []
        probabilities = {}
        qualtities_sum = 0
        population = []

        for i in range(self.size):
            qualities.append(self.specimens[i].quality())
            qualtities_sum.append(self.specimens[i].quality())

        probabilities[0] = [0, qualities[0] / qualtities_sum * 100]
        for i in range(1, self.size - 1):
            probabilities[i] = [probabilities[i - 1][1] + 1,
                                probabilities[i - 1][1] + qualities[i] / qualtities_sum * 100]

        for i in range(self.size):
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


def ea(iterations, time, columns, rows):
    time_ea = 0
    population = Population(columns, rows)
    population.make_population()
    best_specimen = population.specimens[0]

    i = 1
    while i <= iterations:
        population.mutation()
        population.crossover()
        population.selection()
        if population.best_specimen().quality() > best_specimen.quality():
            best_specimen = population.best_specimen()
        time_ea += time.time()
        if time_ea >= time:
            break

    return best_specimen.print()
