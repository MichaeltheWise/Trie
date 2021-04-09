from Trie import Trie
import unittest


class TestTrie(unittest.TestCase):
    def test_search(self):
        tree = Trie.Trie()
        tree.insert("apple")
        tree.insert("apply")

        self.assertEqual(tree.search("app"), False)
        self.assertEqual(tree.search("apple"), True)

    def test_prefix(self):
        tree = Trie.Trie()
        tree.insert("apple")
        tree.insert("apply")

        self.assertEqual(tree.prefix_match("app"), True)
        self.assertEqual(tree.prefix_match("blu"), False)

    def test_prefix_match_list(self):
        tree = Trie.Trie()
        tree.insert("apple")
        tree.insert("apply")
        tree.insert("app")
        tree.insert("blue")

        expected = ['apple', 'apply', 'app']
        actual = tree.prefix_match_list("app")
        self.assertCountEqual(expected, actual)

    def test_full_word_list(self):
        tree = Trie.Trie()
        tree.insert("apple")
        tree.insert("apply")
        tree.insert("blue")
        tree.insert("orange")

        expected = ['orange', 'blue', 'apple', 'apply']
        actual = tree.full_word_list()
        self.assertCountEqual(expected, actual)



