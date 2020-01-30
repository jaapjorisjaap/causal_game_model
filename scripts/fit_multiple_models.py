from genetic_algorithm.genetic_algorithm import genetic_algorithm, Individual
from genetic_algorithm.utils import top_selection, to_png, generate_random_markov_model_with_path, \
    generate_random_markov_model, markov_model_fitness, slow_cross_over, mate_markov_model, mutate_individual
import networkx as nx



def perform_multiple_experiments(n_experiments, n_names, n_repeated_states, number_of_branches, path_length):
    results = []
    for i in range(n_experiments):
        model = generate_model(n_names, n_repeated_states, number_of_branches, path_length)

        fit_function = lambda data: genetic_algorithm(
            lambda size: [Individual(generate_random_markov_model(model.names, number_of_repeated_states)) for i in
                          range(size)],
            pop_size,
            100,
            lambda ind: markov_model_fitness(ind.dna, data),
            lambda pop: top_selection(pop, winner_size),
            lambda pop, pop_size: slow_cross_over(pop, pop_size, mate_markov_model),
            lambda pop: [mutate_individual(i) for i in pop]
        )
        results.append(perform_experiment(model, 20, fit_function, "pop_{}_".format(i)))
    return results

def perform_experiment(model, n_data_points, fit_function, experiment_name):
    '''
    Performs an experiment on a given model
    :param model:
    :param n_data_points:
    :param fit_function:
    :param experiment_name:
    :return: the optimized graph edit distance
    '''

    data = [model.random_walk() for i in range(n_data_points)]
    result, best = fit_function(data)


    to_png(model, "{}_target".format(experiment_name))
    to_png(best.dna, "{}_best".format(experiment_name))
    return min([ x for x in nx.optimize_graph_edit_distance(best.dna.to_di_graph(), model.to_di_graph())])


def generate_model(n_names, number_of_repeated_states, number_of_branches, path_length):


    names = ["start"] + ["{}".format(i) for i in range(n_names)] + ['end']
    return generate_random_markov_model_with_path(names, number_of_repeated_states, path_length, number_of_branches)



number_of_repeated_states = 2
number_of_branches = 2
path_length = 5


pop_size = 30
winner_size = 10

results = perform_multiple_experiments(10, 5, 2, 3, 5)

print(results)



