import time

import matplotlib.pyplot as plt
import numpy as np

import EvolutionaryAlgorithm


def test_permutation_creation_of_specimen(size_of_specimen, max_generated_value):
    # size_of_specimen - size of problem matrix
    # max_generated_value - maximal value of element in matrix

    problem_matrix = np.random.randint(low=0, high=max_generated_value, size=(size_of_specimen, size_of_specimen))
    np.fill_diagonal(problem_matrix, 0)

    S = EvolutionaryAlgorithm.Specimen(problem_matrix)
    print(problem_matrix)
    print("quality: ", S.quality(), "\n")

    start = time.time()
    S.initialize_matrix_permutation()
    S.display()
    print("Time:    ", time.time() - start)
    print("quality: ", S.quality())


def test_change_creation_of_specimen(size_of_specimen, max_generated_value):
    # size_of_specimen - size of problem matrix
    # max_generated_value - maximal value of element in matrix

    problem_matrix = np.random.randint(low=0, high=max_generated_value, size=(size_of_specimen, size_of_specimen))
    np.fill_diagonal(problem_matrix, 0)
    S = EvolutionaryAlgorithm.Specimen(problem_matrix)
    print(problem_matrix)
    print("quality: ", S.quality(), "\n")

    start = time.time()
    S.initialize_matrix_change()
    S.display()
    print("Time:    ", time.time() - start)
    print("quality: ", S.quality())


# TEST make_population method
def test_make_population(size_of_specimen, max_generated_value, size_of_population):
    problem_matrix = np.random.randint(low=0, high=max_generated_value, size=(size_of_specimen, size_of_specimen))
    np.fill_diagonal(problem_matrix, 0)
    start = time.time()
    P = EvolutionaryAlgorithm.Population(size=size_of_population)
    P.make_population(problem_matrix)
    P.display_population()
    print("Time: ", time.time() - start)


def test_time_of_generate_population(max_generated_value):
    size = np.logspace(0, 2, 100).astype('uint8')[10:]
    print(size)
    times = []
    for s in size:
        start = time.time()
        problem_matrix = np.random.randint(low=0, high=max_generated_value, size=(s, s))
        S = EvolutionaryAlgorithm.Specimen(problem_matrix)
        S.initialize_matrix_change()
        times.append(time.time() - start)
    plt.plot(size, times)
    plt.show()


# TEST Evolutionary Algorithm
def test_EA(size_of_specimen, max_generated_value, size_of_population, max_iteration, time_):
    # size_of_specimen - size of problem matrix
    # max_generated_value - maximal value of element in matrix
    # size_of_population - length of specimens
    # max_iteration - maximal number of iteration
    # time_ - time when end algorithm

    # initialize of primitive specimen
    problem_matrix = np.random.randint(low=0, high=max_generated_value, size=(size_of_specimen, size_of_specimen))
    np.fill_diagonal(problem_matrix, 0)
    primitive_specimen = EvolutionaryAlgorithm.Specimen(problem_matrix)
    cols_, rows_ = primitive_specimen.cols, primitive_specimen.rows

    print("columns:", cols_, "\t sum:", np.sum(cols_))
    print("rows:   ", rows_, "\t sum:", np.sum(rows_), "\n")

    # start Evolutionary Algorithm
    start = time.time()
    best_Specimen = EvolutionaryAlgorithm.ea(iterations=max_iteration,
                                             size_of_population=size_of_population,
                                             primitive_specimen=problem_matrix,
                                             time=time_)

    print("\nTime:    ", time.time() - start)

    best_Specimen_cols = np.sum(best_Specimen.matrix, axis=0)
    best_Specimen_rows = np.sum(best_Specimen.matrix, axis=1)

    print("Valid:   ", (best_Specimen_cols == cols_).all() and (best_Specimen_rows == rows_).all())
    print("The best Specimen:")
    best_Specimen.display()

# test_permutation_creation_of_specimen(4, 3)
# test_change_creation_of_specimen(4, 3)

# test_make_population(size_of_specimen=3,
#                      max_generated_value=10,
#                      size_of_population=10)

# test_time_of_generate_population(100)

# test_EA(size_of_specimen=10,
#         max_generated_value=100,
#         size_of_population=20,
#         max_iteration=50,
#         time_=100)
