from genetic_algorithm.genetic_algorithm import *
from genetic_algorithm.utils import *
import matplotlib.pyplot as plt
# The names that we want in the model. start and end will be automaticly added

names = [
    'start',
    'move',
    'a1',
    'a2',
    'end',
]

# How often a state can be repeated.
number_of_repeated_states = 2

#How long (at least one) path should be from start to end
path_length = 4

#how many branches there should be from the path
number_of_branches = 3

#Generates a random model
random_model = generate_random_markov_model_with_path(names, number_of_repeated_states, path_length, number_of_branches)



#Data is created by randomly walking through the model
data = [random_model.random_walk() for i in range(10)]

print(data)