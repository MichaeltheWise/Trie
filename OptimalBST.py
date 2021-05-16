# -*- coding: utf-8 -*-
"""
Created on Sat May 15 2021

@author: Michael Lin
"""
import collections
import functools


# Decorator
def store(func):
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class OptimalBSTSolver:
    def __init__(self, num_range, freq):
        if isinstance(num_range, int) and num_range > 1:
            self.num_range = num_range
        else:
            raise ValueError("num range can only be an integer larger than 1")

        if isinstance(freq, list):
            self.freq = freq
        else:
            raise ValueError("frequency has to be a list")

    def find_distinct_BST_iter(self):
        """
        Find the distinct number of binary search tree using iterative bottom-up dynamic programming technique
        :return: Distinct number of binary search tree
        """
        res = [0] * (self.num_range + 1)
        res[0] = 1
        for i in range(1, self.num_range + 1):
            for j in range(i):
                # An example will be 3 nodes (n = 3)
                # It will be the sum of these combinations
                # dp[0] * dp[2]
                # dp[1] * dp[1]
                # dp[2] * dp[0]
                res[i] += res[j] * res[i - 1 - j]
        return res[self.num_range]

    @store
    def find_distinct_BST_recur(self, num):
        """
        Find the distinct number of binary search tree using memoized top-down recursive dynamic programming technique
        :param num: idx of pivot point
        :return: Distinct number of binary search tree
        """
        if num == 0:
            return 1
        res = 0
        for i in range(num):
            # Left tree contains the distinct number of BST smaller than pivot
            # Right tree contains the distinct number of BST larger than pivot
            left_tree = self.find_distinct_BST_recur(i)
            right_tree = self.find_distinct_BST_recur(num - 1 - i)
            # Can be simplified into:
            # res += self.find_distinct_BST_recur(i) * self.find_distinct_BST_recur(num - 1 - i)
            res += left_tree * right_tree
        return res

    def output_distinct_BST(self):
        """
        Output distinct binary search tree
        :return: List of graphical represented distinct binary search trees
        """
        num_list = list(range(self.num_range))
        # Graphically represent the trees
        return [OptimalBSTSolver.graphicalPrintTree(tree) for tree in self.output_tree_helper(num_list)]

    def output_tree_helper(self, ls):
        if not ls:
            return [None]
        res = []
        # Go through all pivot points
        for i in range(len(ls)):
            # Recursively get list of subtrees smaller than pivot for left subtree
            left_tree = self.output_tree_helper(ls[:i])
            # Recursively get list of subtrees larger than pivot for right subtree
            right_tree = self.output_tree_helper(ls[i+1:])
            for le in left_tree:
                for ri in right_tree:
                    # Create using the list of left and right subtrees
                    new_node = Node(ls[i])
                    new_node.left = le
                    new_node.right = ri
                    res.append(new_node)
        return res

    def optimal_BST_cost_recur(self):
        """
        Output the optimal binary search tree cost using memoized top-down recursive dynamic programming technique
        :return: Minimum binary search tree cost
        """
        return self._optimal_BST_cost_recur(0, len(self.freq) - 1)

    @store
    def _optimal_BST_cost_recur(self, start, end):
        """
        Implementation of recursion
        :param start: starting point for index selection
        :param end: ending point for index selection
        :return: Minimum binary search tree cost
        """
        if end < start:
            return 0
        if start == end:
            return self.freq[start]
        res = float('inf')
        for root in range(start, end + 1):
            # The idea is that:
            # e(i, j) = e(i, r) + e(r+1, j) + sum(p[v] for v in range(i, j)
            # The last term is basically the probability of all the nodes in the interval
            optimal_cost = self._optimal_BST_cost_recur(start, root - 1) + self._optimal_BST_cost_recur(root + 1, end)
            if optimal_cost < res:
                res = optimal_cost
        return res + self.freq_sum(start, end + 1)

    @store
    def freq_sum(self, start, end):
        """
        Memoized way of summing frequency between starting point and ending point
        :param start: starting point
        :param end: ending point
        :return: Sum of frequency
        """
        # This can be replaced by a simple for loop summing all the frequencies between start and end
        if start == end:
            return 0
        return self.freq_sum(start, end-1) + self.freq[end - 1]

    def optimal_BST_cost_iter(self):
        freq_sum, optimal_cost = collections.defaultdict(int), collections.defaultdict(int)
        for i in range(1, len(self.freq) + 1):
            for j in range(len(self.freq) - i + 1):
                k = i + j
                # Calculate the frequency sum between j and k
                freq_sum[j, k] = freq_sum[j, k - 1] + self.freq[k - 1]
                # Calculate the optimal cost using the same formulat in the recursion space
                optimal_cost[j, k] = min(optimal_cost[j, root] + optimal_cost[root + 1, k] for root in range(j, k))
                optimal_cost[j, k] += freq_sum[j, k]
        return optimal_cost[0, len(self.freq)]

    @staticmethod
    def graphicalPrintTree(node):
        """
        Graphical Representation of Binary Tree
        :return: Graphs with format {parent: [child, child...]}
        """
        graph = collections.defaultdict(list)
        if node is not None:
            stack = [node]
            # Graph generation into format {parent: [child, child...]}
            while stack:
                curr = stack.pop(0)
                for child in [curr.left, curr.right]:
                    if child is not None:
                        graph[curr.val].append(child.val)
                        stack.append(child)
        return graph


def main():
    num_range = 3
    freq = [34, 8, 50]
    test_solver = OptimalBSTSolver(num_range, freq)
    print("Distinct BST recursion: {}".format(test_solver.find_distinct_BST_recur(num_range)))
    print("Distinct BST iteration: {}".format(test_solver.find_distinct_BST_iter()))
    print("Distinct BST output: {}".format(test_solver.output_distinct_BST()))
    print("Optimal BST cost recursion: {}".format(test_solver.optimal_BST_cost_recur()))
    print("Optimal BST cost iteration: {}".format(test_solver.optimal_BST_cost_iter()))


if __name__ == '__main__':
    main()
