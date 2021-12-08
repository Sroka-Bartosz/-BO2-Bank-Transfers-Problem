import random

import numpy as np

import functions
import specimen


class Population(specimen.Specimen):
    def __init__(self, size):
        self.specimens = []
        self.elite = []
        self.size = size
        self.best_quality = 0

    def make_population(self, matrix):
        for i in range(self.size):
            S = specimen.Specimen(matrix)
            S.initialize_matrix_change()
            self.specimens.append(S)

    def mutation(self, rows_number=2, cols_number=2):
        random_specimen = random.choice(self.specimens)
        self.specimens.remove(random_specimen)
        random_specimen = random_specimen.matrix

        a = 0
        b = len(random_specimen)
        c = len(random_specimen[0])

        rows = random.sample([i for i in range(a, b)], k=rows_number)
        cols = random.sample([i for i in range(a, c) if i not in rows], k=cols_number)
        temp_matrix_rows = []
        temp_matrix = []
        sum_rows = []
        sum_row = 0
        sum_cols = []
        sum_col = 0
        for i in rows:
            for j in cols:
                temp_matrix_rows.append(random_specimen[j][i])
                sum_row += random_specimen[j][i]
            temp_matrix.append(temp_matrix_rows)
            temp_matrix_rows = []
            sum_rows.append(sum_row)
            sum_row = 0

        for i in cols:
            for j in rows:
                sum_col += random_specimen[i][j]
            sum_cols.append(sum_col)
            sum_col = 0

        temp_matrix = functions.change_matrix(temp_matrix, sum_cols, sum_rows)
        a, b = 0, 0
        for i in rows:
            for j in cols:
                random_specimen[j][i] = temp_matrix[a][b]
                b += 1
            a += 1
            b = 0

        self.specimens.append(specimen.Specimen(random_specimen))

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
        sum_ = 0
        for i in range(len(REM)):
            for j in range(len(REM[0])):
                sum_ += REM[i][j]
            sum_row.append(sum_ / 2)
            sum_ = 0

        sum_col = []
        sum_ = 0
        for i in range(len(REM)):
            for j in range(len(REM[0])):
                sum_ += REM[j][i]
            sum_col.append(sum_ / 2)
            sum_ = 0
        REM1, REM2 = functions.ones(REM)

        self.specimens.append(specimen.Specimen(DIV + REM1))
        self.specimens.append(specimen.Specimen(DIV + REM2))

    def roulette_selection(self):
        qualities = []
        probabilities = {}
        qualities_sum = 0
        population = []

        for i in range(self.size):
            qualities.append(self.specimens[i].quality())
            qualities_sum += (self.specimens[i].quality())
        probabilities[0] = [0, np.ceil(qualities[0] / qualities_sum * 100)]
        for i in range(1, self.size):
            probabilities[i] = [probabilities[i - 1][1],
                                probabilities[i - 1][1] + np.ceil(qualities[i] / qualities_sum * 100)]
        for j in range(self.size):
            rand = np.random.randint(0, probabilities[self.size - 1][1])
            for i in range(self.size):
                if (probabilities[i][0] <= rand) and (probabilities[i][1] >= rand):
                    population.append(self.specimens[i])
                    break
        self.specimens = population

        # if elite:
        #     for j in range(len(self.elite)):
        #         qualities = []
        #         for i in range(self.size):
        #             qualities.append(self.specimens[i].quality())
        #         min_value = min(qualities)
        #         min_index = qualities.index(min_value)
        #         self.specimens[min_index] = self.elite[j]

    def ranking_selection(self):
        qualities = []
        qualities_sum = 0
        population = []
        for i in range(self.size):
            qualities.append(self.specimens[i].quality())
            qualities_sum += (self.specimens[i].quality())
        # print("Q: ", qualities)
        q2 = qualities[:]
        q2.sort()
        # print("Q2: ", q2)
        r = int(0.5 * len(qualities))
        q = q2[-r:][::-1]
        i = 0
        # print("q: ", q)
        while len(population) < self.size:
            for j in range(self.size - 1):
                if qualities[j] == q[i]:
                    population.append(self.specimens[j])
                    break
            i += 1
            if i == len(q) - 1:
                i = 0
        self.specimens = population

        # if elite:
        #     for j in range(len(self.elite)):
        #         qualities = []
        #         for i in range(self.size):
        #             qualities.append(self.specimens[i].quality())
        #         min_value = min(qualities)
        #         min_index = qualities.index(min_value)
        #         self.specimens[min_index] = self.elite[j]



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

        # if elite:
        #     for j in range(len(self.elite)):
        #         qualities = []
        #         for i in range(self.size):
        #             qualities.append(self.specimens[i].quality())
        #         min_value = min(qualities)
        #         min_index = qualities.index(min_value)
        #         self.specimens[min_index] = self.elite[j]

    def best_specimen(self):
        qualities = []

        for i in range(self.size):
            qualities.append(self.specimens[i].quality())

        max_value = max(qualities)
        max_index = qualities.index(max_value)
        return self.specimens[max_index]

    def number_of_specimen(self):
        print(len(self.specimens))

    def sort_specimen_by_quality(self):
        specimens = self.specimens[:]
        specimens.sort(reverse=True, key=lambda s: s.quality())
        return specimens

    def create_elite(self, size_of_elite):
        sorted_specimens = self.sort_specimen_by_quality()
        self.elite = sorted_specimens[:size_of_elite]

    def update_elite(self):
        sorted_specimens = self.sort_specimen_by_quality()
        for e in range(len(self.elite)):
            if sorted_specimens[e].quality() > self.elite[e].quality():
                self.elite[e] = sorted_specimens[e]
            else:
                break

    def display_elite(self):
        for e in self.elite:
            e.display()

    def display_population(self):
        for specimen_ in self.specimens:
            specimen_.display()

    def display_elite_quality(self):
        elite_quality = []
        for e in self.elite:
            elite_quality.append(e.quality())
        print("elite:\t", elite_quality)

    def display_population_quality(self):
        population_quality = []
        for s in self.specimens:
            population_quality.append(s.quality())
        print("population:\t", population_quality)

    def display_quality_changes(self, it):
        best_quality_in_population = self.best_specimen().quality()
        if self.best_quality < best_quality_in_population:
            print("iteration {0} - quality:\t".format(it), best_quality_in_population)
