from collections import deque

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class MarkovModel:
    '''

    Some conventions:
    in a markov model we have the following:
        1) the first name is the starting position
        2) all the names in between the start and the end can be repeated many times in the matrix,
            because we want to allow for multiple states with the same name
        3) the last name is the end position (never should go anywhere)
    '''

    def __init__(self, names, connections):
        self.names = names
        self.connections = connections
        self.repeated_names = [names[0]] + names[1:-1] * self.number_repeated() + [names[-1]]
        numbered_names = []
        for i in range(self.number_repeated()):
            numbered_names += ["{}_{}".format(name, i) for name in names[1:-1]]
        self.repeated_numbered_names = [names[0]] + numbered_names + [names[-1]]

    def to_di_graph(self):
        '''
        Creates a networkx di graph out of the markov model
        :return:
        '''
        edge_list = self.to_edge_list()

        G = nx.DiGraph()
        G.add_weighted_edges_from(edge_list)
        return G

    def show_graph(self):
        nx.draw_kamada_kawai(self.to_di_graph(), with_labels=True, node_size=3000)
        plt.show()

    def add_graph_to_plt(self):
        plt.figure()
        nx.draw_kamada_kawai(self.to_di_graph(), with_labels=True, node_size=3000)

    def to_edge_list(self):
        '''
        Creates an edge list from the graph
        :return:
        '''
        edge_list = []
        for (i, edges) in enumerate(self.connections):

            for (j, e) in enumerate(edges):
                if self.connections[i][j] == 1:
                    n1 = MarkovNode(self.get_name(i), self.get_numbered_name(i))
                    n2 = MarkovNode(self.get_name(j), self.get_numbered_name(j))
                    edge_list.append((n1, n2, 1))
        return edge_list

    def get_one_paths(self):
        '''
        Gets the number of 1 paths through the model
        :return:
        '''
        to_search = deque([{"node": 0, "path_names": [self.get_name(0)], "path": [0]}])
        result = []
        while len(to_search) != 0:
            next_state = to_search.popleft()

            children = self.get_children(next_state["node"])
            added = False
            for child in children:

                if child not in next_state["path"]:
                    new_state = {"node": child, "path_names": next_state["path_names"] + [self.get_name(child)],
                                 "path": next_state["path"] + [child]}
                    to_search.append(new_state)
                    added = True
            if not added:
                result.append([node for node in next_state["path_names"]])
        return result

    def get_name(self, index):
        return self.repeated_names[index]

    def get_index(self, name):
        return self.repeated_numbered_names.index(name)

    def get_numbered_name(self, index):
        return self.repeated_numbered_names[index]

    def number_repeated(self):
        if len(self.names) == 2:
            return 0
        return int((len(self.connections) - 2) / (len(self.names) - 2))

    def add_path(self, names):
        for (n1, n2) in zip(names[:-1], names[1:]):
            i1 = self.get_index(n1)
            i2 = self.get_index(n2)
            self.connections[i1][i2] = 1

    def random_walk(self):
        '''
        Performs a random walk through the graph.
        :return:
        '''
        current_index = 0
        path = [self.repeated_names[current_index]]
        while current_index != len(self.connections) - 1:
            current_index = np.random.choice([i for i, con in enumerate(self.connections[current_index]) if con == 1])
            path.append(self.repeated_names[current_index])

        return path

    def __eq__(self, other):
        return type(self) == type(other) and nx.graph_edit_distance(self.to_di_graph(), other.to_di_graph()) == 0

    def get_size(self):
        return np.sum(self.connections)

    def get_children(self, index):
        return np.argwhere(self.connections[index] == 1).flatten()

    def get_parents(self, index):
        return np.argwhere(self.connections.transpose()[index] == 1).flatten()

    def is_path(self, path):
        if path[0] != "start":
            raise ValueError("Path should begin with start")
        i = 0
        for name in path[1:]:
            children = self.get_children(i)
            names = [self.get_name(child) for child in children]
            if name in names:
                i = children[names.index(name)]
            else:
                return False
        return True

    def match_path_length(self, path):
        count = 0
        if path[0] != "start":
            raise ValueError("Path should begin with start")
        i = 0
        for name in path[1:]:

            children = self.get_children(i)
            names = [self.get_name(child) for child in children]
            if name in names:
                count += 1
                i = children[names.index(name)]
            else:
                return count
        return count


class MarkovNode:

    def __init__(self, name, numbered_name):
        self.name = name
        self.numbered_name = numbered_name

    def __str__(self):
        return self.numbered_name

    def __hash__(self):
        return self.numbered_name.__hash__()

    def __eq__(self, other):
        return type(self) == type(other) and self.numbered_name == other.numbered_name


def collapse(events):
    '''
    Makes a smaller event log by "merging" the same events when they follow each other.
    :param events:
    :return:
    '''
    previous = events[0]
    result = [
        previous
    ]
    for e in events[1:]:
        if e != previous:
            previous = e
            result.append(previous)
    return result


def agrees_with_data(path, collapsed_data):
    '''
    A path agrees with the data if that path is a prefix of a path in the data
    :param path: the path to check if it agrees with the data
    :param data: data that has been collapsed
    :return:
    '''
    for entry in collapsed_data:
        if is_prefix(path, entry):
            return True
    return False


def is_prefix(path_1, path_2):
    '''
    Check path_1 is a prefix of path_2
    :param path_1:
    :param path_2:
    :return:
    '''
    return len(path_1) <= len(path_2) and path_1 == path_2[:len(path_1)]


def array_equals(ar1, ar2):
    if len(ar1) == len(ar2):
        for path in ar1:
            if not path in ar2:
                return False
        return True
    else:
        return False
