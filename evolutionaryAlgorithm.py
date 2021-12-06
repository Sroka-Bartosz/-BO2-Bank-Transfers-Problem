import timeit

import population


def EvolutionaryAlgorithm(iterations, size_of_population, time, primitive_specimen, size_of_elite):
    time_ea, i = 0, 1

    # initialize of population
    population_ = population.Population(size=size_of_population)
    population_.make_population(primitive_specimen)

    # choose first best specimen from initial population
    best_specimen_ = population_.specimens[0]

    # choose first elite
    population_.choose_elite(size_of_elite)

    # run i iterations of algorithm
    while i <= iterations:
        population_.display_elite()

        # get previous elite
        previous_elite = population_.get_previous_elite_quality_list()
        # mutate operator
        [population_.mutation() for i in range(10)]

        # crossover operator
        [population_.crossover() for i in range(10)]

        # selection
        population_.ranking_selection()

        # update elite if better specimen in population
        population_.choose_elite(size_of_elite=size_of_elite, elite=previous_elite)

        # print quality changes
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

    return best_specimen_
