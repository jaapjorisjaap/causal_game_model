import itertools

import numpy as np
import networkx as nx
from genetic_algorithm.genetic_algorithm import Individual
from markov_model.markov_model import MarkovModel, agrees_with_data, collapse


def weighted_selection(population, size=10):
    total = sum([i.fitness for i in population])
    weighted_fitness = [i.fitness / total for i in population]
    return list(np.random.choice(population, size=size, p=weighted_fitness))


def top_selection(population, n=10):
    '''
    Selects the top n fittest individuals
    :param population: popoulation the select the individuals from
    :param n: number of individuals to select.
    :return:
    '''
    sorted_pop = sorted(population, reverse=True, key=lambda i: i.fitness)
    return sorted_pop[:n]


def slow_cross_over(pop, size, mate=None):
    '''
    Slow but easy to program cross over function.
    :param pop:
    :return:
    '''
    choices = [*itertools.product(pop, pop)]
    idx = np.random.choice(len(choices), size)

    choices = [choices[i] for i in idx]
    return [mate(i1, i2) for i1, i2 in choices]


def markov_model_fitness(model, data):
    '''
    The fitness of a model.
        We want models that are small (principle of occam's razor)
        We want models that explain the data (otherwise our model is incorrect)
    :param model: Model to evaluate the fitness of
    :param data: Data to base the fitness on
    :return: The fitness of the model.
    '''

    size = model.get_size()

    total_path_match_length = sum([model.match_path_length(path) for path in data])

    return total_path_match_length - size


def combine_markov_models(m1, m2):
    new_array = np.zeros(m1.connections.shape)
    for i in range(m1.connections.shape[0] - 1):
        for j in range(m1.connections.shape[0]):
            new_array[i, j] = np.random.choice([m1.connections[i, j], m2.connections[i, j]])
    return MarkovModel(m1.names, new_array)


def mate_markov_model(ind1, ind2):
    return Individual(combine_markov_models(ind1.dna, ind2.dna))


def generate_random_markov_model(names, number_of_repeated_states, edge_chance=0.3):
    number_of_states = 2 + (len(names) - 2) * number_of_repeated_states
    shape = (number_of_states, number_of_states)

    random_ar = 1 * (np.random.rand(shape[0] - 1, shape[0]) < edge_chance)

    result = np.vstack((random_ar, np.zeros((1, number_of_states))))
    # Make sure we cannot go back to start
    result[:, 0] = 0

    return MarkovModel(names, result)


def mutate_individual(ind, mutate_chance=0.01):
    return Individual(mutate(ind.dna), mutate_chance)


def mutate(model, mutate_chance=0.01):
    random_ar = 1 * (np.random.rand(model.connections.shape[0] - 1, model.connections.shape[0]) < mutate_chance)
    model_ar = model.connections[:-1, :]
    new_ar = np.logical_xor(model_ar, random_ar)
    result = np.vstack((new_ar, np.zeros((1, model.connections.shape[0]))))

    result[:, 0] = 0
    return MarkovModel(model.names, result)


def generate_random_markov_model_with_path(names, number_of_repeated_states, path_length, number_of_branches):
    n_states = 2 + (len(names) - 2) * number_of_repeated_states
    model = MarkovModel(names, np.zeros((n_states, n_states)))

    repeated__numbered_names = model.repeated_numbered_names
    path = generate_path(repeated__numbered_names[1:-1], path_length)
    correct_path = ["start"] + path + ["end"]

    model.add_path(correct_path)
    for i in range(number_of_branches):
        branch = generate_branch(repeated__numbered_names, correct_path)
        print(branch)
        model.add_path(branch)
    return model


def generate_path(names, path_length):
    return list(np.random.choice(names, path_length, replace=False))


def generate_branch(names, path_names):

    if len(path_names) == 0:
        raise ValueError("Path names is empty")

    first_choice = np.random.choice(path_names[:-1])
    result_path = [first_choice]
    next_state = None
    while next_state not in path_names:
        next_state = np.random.choice(names[1:])

        result_path.append(next_state)
    return result_path


def to_png(model, name):
    pydot_graph_1 = nx.nx_pydot.to_pydot(model.to_di_graph())
    pydot_graph_1.write_png("results/{}.png".format(name))
