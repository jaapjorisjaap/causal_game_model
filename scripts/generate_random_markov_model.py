import numpy as np
import networkx as nx

from genetic_algorithm.utils import mate_markov_model, generate_random_markov_model, mutate, \
    generate_random_markov_model_with_path, to_png
from markov_model.markov_model import MarkovModel

names = ["start"] + ["{}".format(i) for i in range(5)] + ['end']

number_of_repeated_states = 3
number_of_branches = 3
path_length = 5

model = generate_random_markov_model_with_path(names, 2, path_length, number_of_branches)

to_png(model, "generated")

