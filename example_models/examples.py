from markov_model.markov_model import MarkovModel
import numpy as np

one_step = MarkovModel([
    "start",
    "end"
],
    np.array(
        [
            [0, 1],
            [0, 0]
        ])
)

two_step = MarkovModel([
    "start",
    "move",
    "end"
],
    np.array(
        [
            [0, 1, 0],
            [0, 0, 1],
            [0, 0, 0]
        ])
)

repeated = MarkovModel([
    "start",
    "move",
    "end"
],
    np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0]
        ])
)

loop = MarkovModel([
    "start",
    "move",
    "end"
],
    np.array([
        [0, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
    ]
    )
)

branch = MarkovModel([
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
