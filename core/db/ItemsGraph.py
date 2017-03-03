# -*- coding: utf-8 -*-

class ItemGraph:
    """
    Graph of multi edges that represents the connections between
    items. Is a  undirected weighted multi graph
    """

    def __init__(self, items):
        """
        :param items: the array of db orm items
        :return:
        """
        self.items = [x for x in items]

        # a dict of tuples x,y that stores on each pos a list with all edges
        self.adj_matrix = {}

        self._fill_matrix()

    # region Init & Help full

    @property
    def matrix(self):
        """
        :return: the distance matrix as array
        """
        arr = [[-1 if (i, j) not in self.adj_matrix else self.adj_matrix[i, j]
                for j in xrange(len(self.items))]
               for i in xrange(len(self.items))]

        return arr

    def _fill_matrix(self):
        # fill the internal distance matrix

        lenght = len(self.items)
        for i in xrange(lenght):
            for j in xrange(i+1, lenght):

                # the distance mus be symmetric
                distance = self.items[i].distance(self.items[j])

                self.adj_matrix[i, j] = distance
                self.adj_matrix[j, i] = distance

    # endregion

    # region Level Generation

    def sorted_edges(self):
        """
        Method that computes the edges on the graph and sorts them
        :return: list of tuples (item_id, item2_id, distance)
        """
        size = len(self.items)
        edges = [(i, j, self.adj_matrix[i, j]) for i in xrange(size)
                 for j in xrange(i + 1, size) if (i, j) in self.adj_matrix and self.adj_matrix[i, j] >= 0]

        edges.sort(cmp=lambda x,y: cmp(x[2], y[2]))
        return edges

    # region Combinations

    def simple_combination(self):
        """
        Generation of levels by simple combinatory
        :return:
        """

        excluded_dict = dict([(i, False) for i in xrange(len(self.items))])

        data = self.sorted_edges()

        for c in self.combinations_excluded(data, 0, [], 8, excluded_dict):
            yield c

    def combinations_excluded(self, data, index, combination_arr, size, excluded):
        if index == size:
            yield combination_arr

        for x in xrange(index, len(data)):
            i, j, distance = data[x]
            if excluded[i] or excluded[j]:
                continue

            excluded[i], excluded[j] = True, True

            for c in self.combinations_excluded(data, index + 1, combination_arr + [(i, j)], size, excluded):
                yield c

            excluded[i], excluded[j] = False, False

    # endregion

    def shared_coefficient(self, level1, level2):
        """
        Computes the coefficient of repeated items between the two levels
        :param level1: list of tuples (item1, item2)
        :param level2: list of tuples (item1, item2)
        :return: (float) [0, 1]
        """
        items_level1 = [x[0] for x in level1] + [x[1] for x in level1]
        items_level2 = [x[0] for x in level2] + [x[1] for x in level2]

        intersect = set(items_level1).intersection(set(items_level2))

        return len(intersect) * 1.0 / len(items_level1)

    def randomized(self, shared_coeff, levels_size=8, explore_factor=3):
        """
        Generates levels by random exploration.
        :param count: the count of levels to generate
        :param shared_coeff:
        :return:
        """
        data = self.sorted_edges()

        excluded = dict([(i, False) for i in xrange(len(self.items))])

        import random
        levels = []

        # todo improve the constant
        count = len(data) * explore_factor

        for _ in xrange(count):
            comb = []

            while len(comb) < levels_size:
                x = random.randint(0, len(data) - 1)

                i, j, distance = data[x]
                if excluded[i] or excluded[j]:
                    continue

                excluded[i], excluded[j] = True, True
                comb.append((self.items[i], self.items[j]))

            for k in excluded.keys():
                excluded[k] = False

            if len(levels) == 0 or max([self.shared_coefficient(comb, l) for l in levels]) <= shared_coeff:

                levels.append(comb)

        return levels

    # endregion

    def distance(self, item1, item2):
        """
        Gets the distance between two items if any relation exists
        :param item1:
        :param item2:
        :return: distance if items are related (int) -1 otherwise
        """
        try:
            row = self.items.index(item1)
            col = self.items.index(item2)

            # better to say sorry that ask for permission approach
            return self.adj_matrix[row, col]

        except ValueError:
            return -1

    def related(self, item1, item2):
        """
        Checks if two items are related. Shortcut method
        :param item1:
        :param item2:
        :return: True if item1 is related to item2 False otherwise
        """
        return self.distance(item1, item2) >= 0
