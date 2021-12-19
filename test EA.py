import time

import matplotlib.pyplot as plt
import numpy as np

import evolutionaryAlgorithm
import functions
import population
import specimen


def test_permutation_creation_of_specimen(size_of_specimen, max_generated_value):
    # size_of_specimen - size of problem matrix
    # max_generated_value - maximal value of element in matrix

    problem_matrix = np.random.randint(low=0, high=max_generated_value, size=(size_of_specimen, size_of_specimen))
    np.fill_diagonal(problem_matrix, 0)

    S = specimen.Specimen(problem_matrix)
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
    S = specimen.Specimen(problem_matrix)
    print(problem_matrix)
    print("quality: ", S.quality(), "\n")

    cols_, rows_ = S.cols, S.rows

    start = time.time()
    S.initialize_matrix_change()
    S.display()

    init_cols = np.sum(S.matrix, axis=0)
    init_rows = np.sum(S.matrix, axis=1)

    print("Time:    ", time.time() - start)
    print("quality: ", S.quality())
    print("Valid:   ", (init_cols == cols_).all() and (init_rows == rows_).all())


# TEST make_population method
def test_make_population(size_of_specimen, max_generated_value, size_of_population):
    problem_matrix = np.random.randint(low=0, high=max_generated_value, size=(size_of_specimen, size_of_specimen))
    np.fill_diagonal(problem_matrix, 0)
    start = time.time()
    P = population.Population(size=size_of_population)
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
        S = specimen.Specimen(problem_matrix)
        S.initialize_matrix_change()
        times.append(time.time() - start)
    plt.plot(size, times)
    plt.show()


# TEST Evolutionary Algorithm
def random_test_EA(size_of_specimen,
                   max_generated_value,
                   size_of_population: int = 20,
                   iterations: int = 50,
                   time_: int = 1000,
                   size_of_elite: int = 1,
                   number_of_mutations: int = 0,
                   size_of_mutation=[2, 2],
                   number_of_crossover: int = 0,
                   selection_type: str = "roulette"):
    # size_of_specimen - size of problem matrix
    # max_generated_value - maximal value of element in matrix
    # size_of_population - length of specimens
    # iteration = maximal number of iteration
    # time_ - time when end algorithm
    # size_of_elite - length of elite
    # number_of_mutation - parameters defined how many mutation in population was made.
    # selection_type - choose type of selection

    # initialize of primitive specimen
    problem_matrix = functions.initialize_primitive_specimen(size_of_specimen, max_generated_value)
    primitive_specimen = specimen.Specimen(problem_matrix)
    cols_, rows_ = primitive_specimen.cols, primitive_specimen.rows

    print("columns:", cols_, "\t sum:", np.sum(cols_))
    print("rows:   ", rows_, "\t sum:", np.sum(rows_), "\n")

    # start Evolutionary Algorithm
    start = time.time()
    best_Specimen = evolutionaryAlgorithm.EvolutionaryAlgorithm(primitive_specimen=problem_matrix,
                                                                size_of_population=size_of_population,
                                                                iterations=iterations,
                                                                time=time_,
                                                                size_of_elite=size_of_elite,
                                                                number_of_mutations=number_of_mutations,
                                                                size_of_mutation=size_of_mutation,
                                                                number_of_crossover=number_of_crossover,
                                                                selection_type=selection_type)

    print("\nTime:    ", time.time() - start)

    best_Specimen_cols = np.sum(best_Specimen.matrix, axis=0)
    best_Specimen_rows = np.sum(best_Specimen.matrix, axis=1)

    print("Valid:   ", (best_Specimen_cols == cols_).all() and (best_Specimen_rows == rows_).all())
    print("The best Specimen:")
    best_Specimen.display()


# test_permutation_creation_of_specimen(4, 3)
# test_change_creation_of_specimen(4, 3)

# test_make_population(size_of_specimen=12,
#                      max_generated_value=100,
#                      size_of_population=10)

# test_time_of_generate_population(10)

# random_test_EA(size_of_specimen=10,
#                max_generated_value=100,
#                size_of_population=20,
#                iterations=50,
#                # time=10,
#                # size_of_elite=5,
#                number_of_mutations=5,
#                # size_of_mutation=[2,2],
#                number_of_crossover=5,
#                selection_type='tournament')

if __name__ == "__main__":
    problem_matrix = np.array([[0, 16, 7, 39, 47, 27, 22, 2, 90, 0, 46, 95],
                               [19, 0, 41, 0, 78, 8, 3, 19, 58, 10, 41, 26],
                               [61, 48, 0, 8, 53, 46, 43, 67, 28, 3, 0, 37],
                               [80, 35, 51, 0, 73, 94, 1, 0, 57, 75, 8, 13],
                               [95, 31, 1, 15, 0, 46, 94, 9, 50, 56, 0, 94],
                               [25, 36, 34, 78, 31, 0, 94, 6, 69, 0, 17, 7],
                               [11, 91, 23, 8, 25, 93, 0, 27, 34, 29, 0, 9],
                               [69, 8, 36, 23, 64, 1, 85, 0, 27, 61, 37, 0],
                               [20, 26, 15, 14, 3, 63, 6, 44, 0, 9, 32, 97],
                               [72, 38, 5, 18, 3, 10, 61, 63, 16, 0, 9, 16],
                               [84, 9, 48, 18, 6, 53, 7, 55, 67, 40, 0, 72],
                               [13, 24, 23, 8, 0, 5, 39, 0, 33, 81, 51, 0]])

    primitive_specimen = specimen.Specimen(problem_matrix)
    cols_, rows_ = primitive_specimen.cols, primitive_specimen.rows

    print("columns:", cols_, "\t sum:", np.sum(cols_))
    print("rows:   ", rows_, "\t sum:", np.sum(rows_))
    print("\niteration 0 - quality:\t", primitive_specimen.quality())

    # start Evolutionary Algorithm
    start = time.time()
    best_Specimen = evolutionaryAlgorithm.EvolutionaryAlgorithm(primitive_specimen=problem_matrix,
                                                                size_of_population=20,
                                                                iterations=100,
                                                                # time=,
                                                                # size_of_elite=,
                                                                number_of_mutations=5,
                                                                size_of_mutation=[6, 6],
                                                                number_of_crossover=5,
                                                                selection_type="ranking")

    print("\nTime:    ", time.time() - start)

    best_Specimen_cols = np.sum(best_Specimen.matrix, axis=0)
    best_Specimen_rows = np.sum(best_Specimen.matrix, axis=1)

    print("Valid:   ", (best_Specimen_cols == cols_).all() and (best_Specimen_rows == rows_).all())
    print("The best Specimen:")
    best_Specimen.display()
