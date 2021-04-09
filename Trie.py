# -*- coding: utf-8 -*-
"""
Created on Thu Apr 8 2021

@author: Michael Lin
"""


class Node(dict):
    def __init__(self):
        super(Node, self).__init__(self)
        self.__dict__ = self
        # Key for storing the character down the tree
        self.key = None
        # Value is to make sure that we reach the end of the a word
        # A different implementation will be to store an attribute that indicates the end of a word
        self.value = None
        # Children for all the subsequent possible alphabets that the node can connect to
        self.children = {}


class Trie(dict):
    def __init__(self):
        super(Trie, self).__init__(self)
        self.__dict__ = self
        self.root = Node()

    def insert(self, word):
        """
        Insert the word into the trie
        :param word: the word that is going to be insert into this trie
        :return: None
        """
        curr_node = self.root
        for char in word:
            if char in curr_node.children:
                curr_node = curr_node.children[char]
            else:
                new_node = Node()
                new_node.key = char
                curr_node.children[char] = new_node
                curr_node = new_node

        # If end of the word is reached, update the node value here
        # This allows for accurate and exact matching
        curr_node.value = word

    def search(self, word):
        """
        Search for the exact copy of the word
        :param word: the word that one is looking for
        :return: Boolean True/False
        """
        curr_node = self.root
        for char in word:
            if char in curr_node.children:
                curr_node = curr_node.children[char]
            else:
                return False
        # Only if it is an exact match
        if curr_node.value == word:
            return True
        return False

    def prefix_match(self, prefix):
        """
        Search for certain prefix
        :param prefix: the prefix that one is looking for
        :return: Boolean True/False
        """
        curr_node = self.root
        for char in prefix:
            if char in curr_node.children:
                curr_node = curr_node.children[char]
            else:
                return False
        # Don't need an exact match
        return True

    def prefix_match_list(self, prefix):
        """
        List out the words that match the prefix
        :param prefix: the prefix that one wants auto correct with
        :return: List of words
        """
        curr_node = self.root
        if self.prefix_match(prefix=prefix):
            for char in prefix:
                curr_node = curr_node.children[char]
        else:
            print("No Match")
            return None
        # Start traversing from the node where we end up after prefixing
        return Trie.node_traversal(node=curr_node)

    def full_word_list(self):
        """
        List out all the words in this prefix tree
        :return: List of words
        """
        return Trie.node_traversal(node=self.root)

    @staticmethod
    def node_traversal(node):
        """
        Node traversal
        :param node: starting from this node
        :return: None
        """
        res = set()
        queue = [node]
        while queue:
            curr = queue.pop()
            if curr.value is not None and curr.value not in res:
                res.add(curr.value)
            # Similar to other general tree traversals
            # Add in the ones not done yet
            for char in curr.children:
                queue.append(curr.children[char])
        return list(res)


def main():
    tree = Trie()
    print("INSERT: apple")
    tree.insert("apple")
    print("\nSEARCH: apple")
    print("result: {}".format(tree.search("apple")))
    print("\nSEARCH: app")
    print("result: {}".format(tree.search("app")))
    print("\nSEARCH PREFIX: app")
    print("result: {}".format(tree.prefix_match("app")))
    print("\nINSERT: app")
    tree.insert("app")
    print("\nSEARCH: app")
    print("result: {}".format(tree.search("app")))
    print("\nINSERT: apply")
    tree.insert("apply")
    print("\nPREFIX MATCH WORD LIST: app")
    print("result: {}".format(tree.prefix_match_list("app")))
    print("\nINSERT: ball")
    tree.insert("ball")
    print("\nFULL WORD LIST:")
    print("result: {}".format(tree.full_word_list()))


if __name__ == "__main__":
    main()

