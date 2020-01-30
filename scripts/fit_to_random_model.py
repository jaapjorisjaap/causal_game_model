import numpy as np
import networkx as nx
from genetic_algorithm.genetic_algorithm import genetic_algorithm, Individual
from genetic_algorithm.utils import mate_markov_model, generate_random_markov_model, mutate, \
    generate_random_markov_model_with_path, to_png, markov_model_fitness, top_selection, slow_cross_over, \
    mutate_individual
from markov_model.markov_model import MarkovModel, collapse

names = ["start"] + ["{}".format(i) for i in range(5)] + ['end']

number_of_repeated_states = 2
number_of_branches = 2
path_length = 5

model = generate_random_markov_model_with_path(names, number_of_repeated_states, path_length, number_of_branches)

data = [model.random_walk() for i in range(10)]


names = model.names


pop_size = 30
winner_size = 5
repeated_names = 2

result, best = genetic_algorithm(
    lambda size: [Individual(generate_random_markov_model(names, number_of_repeated_states)) for i in range(size)],
    pop_size,
    100,
    lambda ind: markov_model_fitness(ind.dna, data),
    lambda pop: top_selection(pop, winner_size),
    lambda pop, pop_size: slow_cross_over(pop, pop_size, mate_markov_model),
    lambda pop: [mutate_individual(i) for i in pop]
)

winners = top_selection(result, 1)


to_png(model, "target")
to_png(best.dna, "best")
for i, r in enumerate(winners):
    to_png(r.dna, i)
    print( nx.graph_edit_distance(r.dna.to_di_graph(), model.to_di_graph()))
print(result)
