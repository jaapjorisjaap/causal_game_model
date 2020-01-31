
#Script that shows how you can create a model
from markov_model.markov_model import MarkovModel
import numpy as np

# First of all a model has names, and a matrix representing the transition.
# The row should have no arrows in it.
# Furthermore because a state (except for start and end) can be repeated so we repeat those also in the matrix.
branching_model = MarkovModel([
    "start",
    "a",
    "b1",
    "b2",
    "end"
],
    np.array(
        [
            [0, 1, 0, 0, 1, 0, 0, 0],  # start
            [0, 0, 1, 0, 0, 0, 0, 0],  # a_1
            [0, 0, 0, 0, 0, 0, 0, 1],  # b1_1
            [0, 0, 0, 0, 0, 0, 0, 1],  # b2_1
            [0, 0, 0, 1, 0, 0, 0, 0],  # a_2
            [0, 0, 0, 0, 0, 0, 0, 0],  # b1_2
            [0, 0, 0, 0, 0, 0, 0, 0],  # b2_2
            [0, 0, 0, 0, 0, 0, 0, 0],  # end
        ]
    )
)


#Then we can show the graph

branching_model.show_graph()


