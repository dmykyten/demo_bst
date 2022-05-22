"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log
import random
import timeit
import sys

sys.setrecursionlimit(15000)

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourcecollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourcecollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            strline = ""
            if node is not None:
                strline += recurse(node.right, level + 1)
                strline += "| " * level
                strline += str(node.data) + "\n"
                strline += recurse(node.left, level + 1)
            return strline

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        nodes = []

        def recurse(node):
            if node is not None:
                nodes.append(node.data)
                recurse(node.left)
                recurse(node.right)

        recurse(self._root)
        return iter(nodes)

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        nodes = []

        def recurse(node):
            if node is not None:
                recurse(node.left)
                recurse(node.right)
                nodes.append(node.data)

        recurse(self._root)
        return iter(nodes)

    # def levelorder(self):
    #     """Supports a levelorder traversal on a view of self."""
    #     nodes = set()
    #     def get_childen_with_root(node):
    #         children = [node, node.left, node.right]
    #         return [child for child in children if child is not None]
    #
    #     def recurse(node):
    #         if node != None:
    #             nodes_to_append = [curnode.data for curnode in get_childen_with_root(node)]
    #             for curnode in nodes_to_append:
    #                 nodes.add(curnode)
    #             recurse(node.left)
    #             recurse(node.right)
    #
    #     recurse(self._root)
    #     return iter(nodes)

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    def find_norec(self, item):
        successors = [self._root]
        for node in successors:
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                successors.append(node.left)
            else:
                successors.append(node.right)

    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    # Mutator methods

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1
        print(self._size)


    def add_norec(self, item):
        """Adds item to the tree."""

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            successors = [self._root]
            for node in successors:
                if item < node.data:
                    if node.left is None:
                        node.left = BSTNode(item)
                    else:
                        successors.append(node.left)
                # New item is greater or equal,
                # go right until spot is found
                elif node.right is None:
                    node.right = BSTNode(item)
                else:
                    successors.append(node.right)
                # End of recurse
        self._size += 1


    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if item not in self:
            raise KeyError("Item not in tree." "")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentnode = top.left
            while currentnode.right is not None:
                parent = currentnode
                currentnode = currentnode.right
            top.data = currentnode.data
            if parent == top:
                top.left = currentnode.left
            else:
                parent.right = currentnode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = "L"
        current_node = self._root
        while current_node is not None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = "L"
                current_node = current_node.left
            else:
                direction = "R"
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if current_node.left is not None and current_node.right is not None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == "L":
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    @staticmethod
    def _is_leaf(node):
        if node.left is None and node.right is None:
            return True
        else:
            return False

    def height(self):
        """
        Return the height of tree
        :return: int
        """

        def height1(top):  # time is linear in size of subtree
            """Return the height of the subtree rooted at Position p."""
            if self._is_leaf(top):
                return 0
            else:
                children = [top.left, top.right]
                return 1 + max(height1(child) for child in children if child is not None)

        return height1(self._root)

    def is_balanced(self):
        """
        Return True if tree is balanced
        :return:
        """
        balanced = self.height() < 2 * log(len(list(self.inorder())), 2) - 1
        return balanced

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        return [item for item in self.inorder() if low <= item <= high]

    def rebalance(self):
        """
        Rebalances the tree.
        :return:
        """
        nodes = list(self.inorder())

        def recurse():
            middle = len(nodes) // 2
            if len(nodes) != 0:
                node = nodes.pop(middle)
                self.add(node)
                recurse()

        self.clear()
        recurse()

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        larger_than = [node for node in self.inorder() if node > item]
        return min(larger_than) if len(larger_than) != 0 else None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        smaller_than = [node for node in self.inorder() if node < item]
        return max(smaller_than) if len(smaller_than) != 0 else None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """

        LIMIT = 10000

        def read_data():
            with open(path, 'r') as f:
                return [line.strip() for line in f.readlines()]

        def get_random_words():
            return random.sample(main_data, LIMIT)

        main_data = read_data()

        def case1():
            print('case 1, builtin list, time: ', end='')
            case_data = sorted(main_data)
            start = timeit.default_timer()
            for word in random_list:
                case_data.index(word)
            end = timeit.default_timer()
            print(end - start)

        def case2():
            print('Wait, next case is slow :(')
            case_data = sorted(main_data)

            # generate and fill tree
            tree = LinkedBST()
            for word in case_data:
                # rewrote method because of recursion problem
                tree.add_norec(word)


            print('case 2, BS tree from sorted list, unbalanced + non recursive insertion and search, time: ', end='')
            start = timeit.default_timer()
            for word in random_list:
                tree.find_norec(word)
            end = timeit.default_timer()
            print(end - start)
            print('BAD!')

        def case3():
            case_data = main_data
            random.shuffle(case_data)
            # generate and fill tree
            tree = LinkedBST()
            for word in case_data:
                # rewrote method because of recursion problem
                tree.add_norec(word)

            print('case 3, BS tree from shuffled list + non recursive insertion and search, time: ', end='')
            start = timeit.default_timer()
            for word in random_list:
                tree.find_norec(word)
            end = timeit.default_timer()
            print(end - start)
            print('Rly fast, WOW!')

        def case4():
            case_data = main_data
            # generate and fill tree
            tree = LinkedBST()
            for word in case_data:
                # rewrote method because of recursion problem
                tree.add_norec(word)

            tree.rebalance()
            print('case 5, balanced BS tree + non recursive insertion and search, time: ', end='')
            start = timeit.default_timer()
            for word in random_list:
                tree.find_norec(word)
            end = timeit.default_timer()
            print(end - start)
            print('Rly fast, WOW!')

        print('each case limit is:', LIMIT)
        random_list = get_random_words()
        case1()
        case2()
        case3()
        # haven't implemented non recursive rebalance properly :(
        # case4()




b = LinkedBST()
b.demo_bst('words.txt')
