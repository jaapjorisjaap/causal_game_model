import unittest

from example_models.examples import *
import networkx as nx

from markov_model.markov_model import MarkovNode


class TestMarkovModel(unittest.TestCase):

    def test_add_path(self):
        model = MarkovModel(branch.names, np.zeros((10, 10)))
        model.add_path(["start", "a_0", "b1_0", "end"])
        model.add_path(["start", "a_1", "b1_1", "end"])

        self.assertEqual(model, branch)

    def test_to_edge_list(self):
        tests = [
            (one_step, [(MarkovNode('start', 'start'), MarkovNode('end', 'end'), 1)]),

        ]
        for model, expected in tests:
            self.edge_list_test(model, expected)

    def edge_list_test(self, model, expected):
        edge_list = model.to_edge_list()

        self.assertEqual(set(edge_list), set(expected))

    def test_get_name(self):
        tests = [
            (two_step, 1, 'move'),
            (repeated, 2, 'move')
        ]
        for (model, index, expected) in tests:
            self.get_name_test(model, index, expected)

    def get_name_test(self, model, index, expected):
        name = model.get_name(index)
        self.assertEqual(name, expected)

    def test_get_numbered_name(self):
        tests = [
            (two_step, 1, 'move_0'),
            (repeated, 2, 'move_1')
        ]
        for (model, index, expected) in tests:
            self.get_numbered_name_test(model, index, expected)

    def get_numbered_name_test(self, model, index, expected):
        name = model.get_numbered_name(index)
        self.assertEqual(name, expected)

    def test_get_di_graph(self):
        G_expected = nx.DiGraph()
        edges = [
            ('start', 'move_0', 1),
            ('move_0', 'move_1', 1),
            ('move_1', 'end', 1),

        ]

        G_expected.add_weighted_edges_from(edges)
        self.assertEqual(nx.graph_edit_distance(G_expected, repeated.to_di_graph()), 0)

    def test_get_size(self):
        tests = [
            (one_step, 1),
            (two_step, 2),
            (repeated, 3)

        ]

        for (model, expected_size) in tests:
            self.assertEqual(model.get_size(), expected_size)

    def test_is_path(self):
        tests = [
            (one_step, ["start", "end"], True),
            (one_step, ["start", "move", "end"], False),
            (two_step, ["start", "move", "end"], True),
            (repeated, ["start", "move", "move", "end"], True),
            (repeated, ["start", "move", "move", "move", "end"], False),
            (loop, ["start", "move", "move", "move", "end"], True)
        ]

        for model, path, expected in tests:
            self.assertEqual(model.is_path(path), expected, "{} is not a path in the model".format(path))

    def test_get_children(self):
        tests = [
            (one_step, 0, [1]),
            (two_step, 1, [2]),
            (repeated, 1, [2]),
            (loop, 1, [1, 2])
        ]

        for model, parent, expected in tests:
            self.assertEqual(set(model.get_children(parent)), set(expected))

    def test_get_parents(self):
        tests = [
            (one_step, 0, []),
            (two_step, 1, [0]),
            (repeated, 2, [1]),
            (loop, 1, [1, 0])
        ]

        for model, child, expected in tests:
            self.assertEqual(set(model.get_parents(child)), set(expected))


    def test_get_one_paths(self):
        tests =[
            (one_step, [["start", "end"]]),
            (two_step, [["start", "move", "end"]]),
            (repeated, [["start", "move", "move", "end"]]),
            (loop, [["start", "move", "end"]] ),
            (branch, [["start", "a", "b1", "end"], ["start", "a", "b2",  "end"]])
        ]

        for model, expected in tests:
            self.assertEqual(model.get_one_paths(), expected)

