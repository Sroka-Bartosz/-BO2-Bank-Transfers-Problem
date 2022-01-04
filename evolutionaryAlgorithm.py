import timeit
from typing import List

import population


def EvolutionaryAlgorithm(
        primitive_specimen,
        size_of_population: int = 20,
        iterations: int = 50,
        time: int = 1000,
        size_of_elite: int = 1,
        number_of_mutations: int = 0,
        size_of_mutation: List = [2, 2],
        number_of_crossover: int = 0,
        selection_type: str = "roulette"):
    time_ea, i = 0, 1

    # initialize of population
    population_ = population.Population(size=size_of_population)
    population_.make_population(primitive_specimen)

    # choose first best specimen from initial population
    best_specimen_ = population_.specimens[0]

    # create elite
    population_.create_elite(size_of_elite=size_of_elite)

    # run i iterations of algorithm
    while i <= iterations:
        # mutation
        [population_.mutation(size_of_mutation[0], size_of_mutation[1]) for i in range(number_of_mutations)]

        # crossover
        [population_.crossover() for i in range(number_of_crossover)]

        # selection
        population_.selection(selection_type=selection_type)

        # update elite if better specimen in population
        population_.update_elite()

        # print quality changes
        # population_.display_elite_quality()
        # population_.display_population_quality()
        population_.display_quality_changes(i)

        # get new best specimen
        if population_.best_specimen().quality() > population_.best_quality:
            best_specimen_ = population_.best_specimen()
            population_.best_quality = best_specimen_.quality()

        # time stop condition
        time_ea += timeit.timeit()
        if time_ea >= time:
            break
        i += 1

    return best_specimen_, population_.global_quality
