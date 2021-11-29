import time

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
def filter(permutation, columns):
    pop_idx = []
    for idx_p in range(len(permutation)):
        if (np.array((permutation[idx_p])) > np.array(columns)).any():
            pop_idx.append(idx_p)
    for idx in pop_idx[::-1]:
        permutation.pop(idx)
    return permutation


# def rows_generator(size, sum_of_rows):
#     values = [0, sum_of_rows] + list(np.random.randint(low=0, high=sum_of_rows, size=size - 1))
#     values.sort()
#     return [values[i + 1] - values[i] for i in range(size)]


class Specimen:
    def __init__(self, size):
        self.matrix = np.zeros((size, size))
        self.size = size

    def initialize_matrix(self, columns, rows):
        start = time.time()
        while True:
            for row in range(self.size):
                permutation = list(sums(self.size, rows[row]))
                rows_ = filter(permutation, columns)
                idx_random_row = np.random.randint(len(rows_))
                self.matrix[row] = rows_[idx_random_row]
            if list(np.sum(self.matrix, axis=0)) == columns:
                print(self.matrix)
                print(time.time() - start, "\n")
                break

    def initialize_matrix2(self, columns, rows):
        start = time.time()
        it = 0

        # Obliczenie pierwszego wiersza
        first_rows = filter(list(sums(self.size, rows[0])), columns)
        while len(first_rows) > 0:
            temp_columns = columns
            idx_random_row = np.random.randint(len(first_rows))
            first_row = first_rows[idx_random_row]
            self.matrix[0] = first_row
            first_rows.pop(idx_random_row)

            # Obliczenie drugiego wiersza
            temp_columns = [temp_columns[i] - first_row[i] for i in range(self.size)]
            second_rows = filter(list(sums(self.size, rows[1])), temp_columns)
            while len(second_rows) > 0:
                temp_columns2 = temp_columns
                idx_random_row = np.random.randint(len(second_rows))
                second_row = second_rows[idx_random_row]
                self.matrix[1] = second_row
                second_rows.pop(idx_random_row)

                # Obliczenie ostatniego wiersza
                temp_columns2 = [temp_columns2[i] - second_row[i] for i in range(self.size)]
                self.matrix[2] = temp_columns2

                # Znalezienie poprawnego osobnika
                if list(np.sum(self.matrix, axis=0)) == columns:
                    print(self.matrix)
                    it += 1
                    break
        print(time.time() - start)
        print("ilość znalezionych osobników", it)

    # def make_matrix(self, columns, rows):
    #     start = time.time()
    #     while True:
    #         self.matrix = np.array([rows_generator(self.size, rows[row]) for row in range(len(rows))])
    #         print(self.matrix)
    #         if list(np.sum(self.matrix, axis=0)) == columns:
    #             stop = time.time()
    #             break
    #
    #     print(stop - start)

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
