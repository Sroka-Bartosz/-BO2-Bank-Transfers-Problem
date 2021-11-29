import time

import numpy as np

import EvolutionaryAlgorithm


# TEST initialize_matrix() method

# TEST 1
def test1():
    S = EvolutionaryAlgorithm.Specimen(3)
    rows_ = [2,
             2,
             2]
    columns_ = [1, 2, 3]
    start = time.time()
    S.initialize_matrix(columns_, rows_)
    S.display()
    print("Time:    ", time.time() - start)
    print("quality: ", S.quality())


# TEST 2
def test2():
    S = EvolutionaryAlgorithm.Specimen(6)
    columns_ = [6, 8, 9, 6, 3, 7]
    rows_ = [8, 3, 7, 9, 8, 4]
    start = time.time()
    S.initialize_matrix(columns_, rows_)
    S.display()
    print("Time:    ", time.time() - start)
    print("quality: ", S.quality())


def random_test(size, max):
    # size - size of problem matrix
    # max - maximal value of element in sum of columns/rows

    columns_ = list(np.random.randint(low=0, high=max, size=size))
    rows_ = list(np.sort(columns_))
    S = EvolutionaryAlgorithm.Specimen(size)
    start = time.time()
    S.initialize_matrix(columns_, rows_)
    S.display()
    print("Time:    ", time.time() - start)
    print("quality: ", S.quality())


# test1()
test2()


# random_test(size=6, max=20)

# TEST make_population method
def test_population_make():
    columns_ = [6, 8, 9, 6, 3, 7]
    rows_ = [8, 3, 7, 9, 8, 4]
    start = time.time()
    P = EvolutionaryAlgorithm.Population(columns_, rows_, 20)
    P.make_population()
    P.display_population()
    print("Time: ", time.time() - start)

# test_population_make()
