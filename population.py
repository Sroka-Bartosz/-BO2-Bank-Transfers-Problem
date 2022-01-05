import copy
import random

import numpy as np

import functions
import specimen


def elementary_crossover(parent1_, parent2_):
    parent1 = parent1_.matrix
    parent2 = parent2_.matrix
    DIV = (parent1 + parent2) // 2
    REM = (parent1 + parent2) % 2

    REM1, REM2 = functions.ones(REM)
    if REM1 + REM2 is not REM:
        child1 = parent1_
        child2 = parent2_
    else:
        child1 = specimen.Specimen(DIV + REM1)
        child2 = specimen.Specimen(DIV + REM2)
    return child1, child2


def elementary_mutation(mutate_specimen, rows_number, cols_number):
    rows = random.sample([i for i in range(mutate_specimen.number_of_rows)], k=rows_number)
    cols = random.sample([i for i in range(mutate_specimen.number_of_cols) if i not in rows], k=cols_number)

    mutate_specimen = mutate_specimen.matrix

    temp_matrix_rows = []
    temp_matrix = []
    sum_rows = []
    sum_row = 0
    sum_cols = []
    sum_col = 0
    for i in rows:
        for j in cols:
            temp_matrix_rows.append(mutate_specimen[j][i])
            sum_row += mutate_specimen[j][i]
        temp_matrix.append(temp_matrix_rows)
        temp_matrix_rows = []
        sum_rows.append(sum_row)
        sum_row = 0

    for i in cols:
        for j in rows:
            sum_col += mutate_specimen[i][j]
        sum_cols.append(sum_col)
        sum_col = 0

    temp_matrix = functions.change_matrix(temp_matrix, sum_cols, sum_rows)
    a, b = 0, 0
    for i in rows:
        for j in cols:
            mutate_specimen[j][i] = temp_matrix[a][b]
            b += 1
        a += 1
        b = 0
    return mutate_specimen


class Population(specimen.Specimen):
    def __init__(self, size):
        self.specimens = []
        self.elite = []
        self.size = size
        self.best_quality = 0
        self.global_quality = []

    def make_population(self, matrix):
        for i in range(self.size):
            if i == 0:
                S = specimen.Specimen(functions.reshape_initial_problem(matrix))
            else:
                S = specimen.Specimen(matrix)
                S.initialize_matrix_change()
            self.specimens.append(S)

    def choose_specimen_to_mutation(self):
        random_specimen = random.choice(self.specimens)
        while random_specimen in self.elite:
            random_specimen = random.choice(self.specimens)
        self.specimens.remove(random_specimen)
        return random_specimen

    def mutation(self, rows_number=2, cols_number=2):
        random_specimen = self.choose_specimen_to_mutation()
        mutate_specimen = elementary_mutation(random_specimen, rows_number=rows_number, cols_number=cols_number)
        self.specimens.append(specimen.Specimen(mutate_specimen))

    def choose_parent_to_crossover(self):
        parent1_ = random.choice(self.specimens)
        self.specimens.remove(parent1_)
        parent2_ = random.choice(self.specimens)
        self.specimens.remove(parent2_)
        return parent1_, parent2_

    def crossover(self):
        crossover_parent1, crossover_parent2 = self.choose_parent_to_crossover()
        crossover_child1, crossover_child2 = elementary_crossover(crossover_parent1, crossover_parent2)
        self.specimens.append(crossover_child1)
        self.specimens.append(crossover_child2)

    def selection(self, selection_type):
        if not isinstance(selection_type, str):
            raise Exception('ERROR: incorrect type of selection_type want str, got {0}'.format(type(selection_type)))
        self.specimens = [s for s in self.specimens if s not in self.elite]
        self.size = self.size - len(self.elite)
        if selection_type == 'roulette':
            self.roulette_selection()
        elif selection_type == 'ranking':
            self.ranking_selection()
        elif selection_type == 'tournament':
            self.tournament_selection()
        else:
            raise ValueError('ERROR: incorrect type of selection, choose one from [roulette, ranking, tournament]')
        self.specimens = self.specimens + self.elite
        self.size = self.size + len(self.elite)

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

    def number_of_specimen(self):
        print(len(self.specimens))

    def sort_specimen_by_quality(self):
        specimens = self.specimens[:]
        specimens.sort(reverse=True, key=lambda s: s.quality())
        return specimens

    def create_elite(self, size_of_elite):
        sorted_specimens = self.sort_specimen_by_quality()
        self.elite = copy.deepcopy(sorted_specimens[:size_of_elite])

    def update_elite(self):
        sorted_specimens = self.sort_specimen_by_quality()
        for e in range(len(self.elite)):
            if sorted_specimens[e].quality() > self.elite[e].quality():
                self.elite[e] = copy.deepcopy(sorted_specimens[e])
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
            self.global_quality.append([it, best_quality_in_population])
            print("iteration {0} - quality:\t".format(it), best_quality_in_population)
