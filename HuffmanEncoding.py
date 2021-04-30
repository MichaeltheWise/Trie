# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 2021

@author: Michael Lin
"""
import collections
import heapq
from itertools import count


class Node:
    def __init__(self):
        self.key = None
        self.val = None
        self.left = None
        self.right = None


class HuffmanEncoder:
    def __init__(self, seq, freq):
        self.seq = seq
        self.freq = freq
        self.num = count()

    def transform(self):
        """
        Transform into zip format
        :return: Zip format with (frequency, counter, tree)
        """
        node_list = []
        for i in range(len(self.seq)):
            new_node = Node()
            new_node.key = self.seq[i]
            new_node.val = self.freq[i]
            node_list.append(new_node)
        return list(zip(self.freq, self.num, node_list))

    def huffman_encoding(self):
        """
        Encode using Huffman Algorithm
        :return: Huffman encoding tree
        """
        res = self.transform()
        heapq.heapify(res)
        while len(res) > 1:
            val_a, _, node_a = heapq.heappop(res)
            val_b, _, node_b = heapq.heappop(res)
            new_node = Node()
            new_node.key = None
            new_node.val = val_a + val_b
            new_node.left = node_a
            new_node.right = node_b
            heapq.heappush(res, (val_a + val_b, next(self.num), new_node))
        return res[0][-1]


class HuffmanDecoder:
    def __init__(self, tree):
        self.tree = tree

    def mapping(self):
        """
        Use input tree to extract encoding scheme
        :return: Encoding scheme
        """
        prefix_dict = {}
        stack = [(self.tree, '')]
        while stack:
            curr, prefix = stack.pop(0)
            for child, bit in [(curr.left, '0'), (curr.right, '1')]:
                if child is not None:
                    if child.key is not None:
                        prefix_dict[child.key] = prefix + bit
                    stack.append((child, prefix + bit))
        return prefix_dict

    def huffman_decoding(self, seq, tree):
        """
        Use existing Huffman encoding tree to decode messages
        :param seq: encoded message
        :param tree: Huffman encoding tree
        :return: Decoded message
        """
        root, res = tree, ''
        while len(seq) > 0:
            while root.key is None:
                if int(seq[0]) == 0:
                    root = root.left
                else:
                    root = root.right
                seq = seq[1:]
            res += root.key
            root = tree
        return res


def graphicalPrintTree(tree):
    """
    Graphical Representation of Binary Tree
    :param tree: tree
    :return: Graphs with format {parent: [child, child...]}
    """
    graph = collections.defaultdict(list)
    stack = [tree]
    # Graph generation into format {parent: [child, child...]}
    while stack:
        curr = stack.pop(0)
        for child in [curr.left, curr.right]:
            if child is not None:
                graph[curr.val].append((child.val, child.key))
                stack.append(child)
    return graph


def main():
    seq = 'abcdefghi'
    freq = [4, 5, 6, 9, 11, 12, 15, 16, 20]
    test_huffman_encoder = HuffmanEncoder(seq, freq)
    print("Full tree graphical representation: ")
    print(graphicalPrintTree(test_huffman_encoder.huffman_encoding()))

    print("\nEncoding scheme: ")
    test_huffman_decoder = HuffmanDecoder(test_huffman_encoder.huffman_encoding())
    print(test_huffman_decoder.mapping())
    encoded_msg = '0100101011'
    print("\nDecoding message {}".format(encoded_msg))
    print(test_huffman_decoder.huffman_decoding(encoded_msg, test_huffman_encoder.huffman_encoding()))


if __name__ == '__main__':
    main()
