import math


def genetic_algorithm(initialize_population, pop_size, n_no_improve_rounds, fitness_function, select_winners,
                      cross_over,
                      mutate):
    """
    A genetic algorithm that
    :param initialize_population: function to initialize the population
    :param pop_size: the size of the population
    :param no_improve_round: number of round that we allow for not improving, if there is no improvement
    :param fitness_function: A function that finds the fitness of the individual
    :param select_winners: A function that select the winners of the population
    :param cross_over: A function that does the cross over of the winners
    :param mutate: A function that mutates a winner
    :return: The population when there is no improvement for n_no_improve_round and the best individual found sofar
    """
    current_population = initialize_population(pop_size)
    max_fitness = - math.inf
    best_i = None
    for i in current_population:
        i.fitness = fitness_function(i)
        if i.fitness > max_fitness:
            max_fitness = i.fitness

    count = 0
    rounds_not_improved = 0

    while rounds_not_improved < n_no_improve_rounds:
        count += 1

        winners = select_winners(current_population)

        new_population = cross_over(winners, pop_size)

        new_population = mutate(new_population)

        current_population = new_population

        for i in current_population:

            i.fitness = fitness_function(i)
            if i.fitness > max_fitness:
                max_fitness = i.fitness
                best_i = i
                rounds_not_improved = 0

        rounds_not_improved += 1
        if count % 10 == 0:
            print(max_fitness)

    return (current_population, best_i)


class Individual:

    def __init__(self, dna, fitness=None):
        self.dna = dna
        self.fitness = fitness
        self.weighted_fitness = None
        self.diversity_score = 0

    def __str__(self):
        return str(self.dna)
