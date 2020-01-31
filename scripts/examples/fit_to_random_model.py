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

random_model = generate_random_markov_model_with_path(names, number_of_repeated_states, path_length, number_of_branches)




data = [random_model.random_walk() for i in range(10)]

pop_size = 50
winner_size = 5

last_population, best = genetic_algorithm(
            lambda size: [Individual(generate_random_markov_model(random_model.names, number_of_repeated_states)) for i in
                          range(size)],
            pop_size,
            50,
            lambda ind: markov_model_fitness(ind.dna, data),
            lambda pop: top_selection(pop, winner_size),
            lambda pop, pop_size: slow_cross_over(pop, pop_size, mate_markov_model),
            lambda pop: [mutate_individual(i) for i in pop]
        )

random_model.add_graph_to_plt()
best.dna.add_graph_to_plt()
plt.show()