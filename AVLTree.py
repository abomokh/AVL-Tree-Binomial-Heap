# username - Abomokh
# id1      - 315270678
# name1    - Abomokh
# id2      - 324262914
# name2    - Amalhaj


"""A class represnting a node in an AVL tree"""



class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int or None
    @param key: key of your node
    @type value: any
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        if key is None:
            self.left = None
            self.right = None
            self.parent = None
            self.height = -1
            self.size = 0
        else:
            self.left = AVLNode(None, None)
            self.right = AVLNode(None, None)
            self.left.parent = self
            self.right.parent = self
            self.parent = None
            self.update_height()
            self.update_size()

    """returns the key

    @rtype: int or None
    @returns: the key of self, None if the node is virtual
    """

    def get_key(self):
        return self.key

    """returns the value

    @rtype: any
    @returns: the value of self, None if the node is virtual
    """

    def get_value(self):
        return self.value

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child (if self is virtual)
    """

    def get_left(self):
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child (if self is virtual)
    """

    def get_right(self):
        return self.right

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def get_parent(self):
        return self.parent

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def get_height(self):
        return self.height

    """returns the size of the subtree

    @rtype: int
    @returns: the size of the subtree of self, 0 if the node is virtual
    """

    def get_size(self):
        return self.size

    """sets key

    @type key: int or None
    @param key: key
    """

    def set_key(self, key):
        self.key = key

    """sets value

    @type value: any
    @param value: data
    """

    def set_value(self, value):
        self.value = value

    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def set_left(self, node):
        if self.is_real_node() is False:
            return None

        if node is None:
            self.set_left(AVLNode(None, None))

        # self.left.set_parent(None)
        self.left = node
        self.left.set_parent(self)
        self.update_fields()

        return None

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def set_right(self, node):
        if self.is_real_node() is False:
            return None

        if node is None:
            self.set_right(AVLNode(None, None))

        # self.right.set_parent(None)
        self.right = node
        self.right.set_parent(self)
        self.update_fields()

        return None

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def set_parent(self, node):
        if self:
            self.parent = node

    """sets the height of the node

    @type h: int
    @param h: the height
    """

    def set_height(self, h):
        self.height = h
        return None

    def update_height(self):
        if self.is_real_node is False:
            self.set_height(-1)
            return None
        self.set_height(max(self.right.get_height(), self.left.get_height()) + 1)

        return None

    """sets the size of node

    @type s: int
    @param s: the size
    """

    def set_size(self, s):
        self.size = s
        return None

    def update_size(self):
        if self.is_real_node is False:
            self.set_size(0)
            return None
        self.set_size(self.right.get_size() + self.left.get_size() + 1)

        return None

    def update_fields(self):
        self.update_size()
        self.update_height()

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        if not self:
            return False
        if self.key is not None:
            return True
        return False

    def get_BF(self):
        if self.is_real_node():
            return self.get_left().get_height() - self.get_right().get_height()

    def is_right_child(self, node):
        return self.get_right() is node

    def has_left_child(self):
        return self.get_left().is_real_node()

    def has_right_child(self):
        return self.get_right().is_real_node()

    def is_leaf(self):
        return (not self.get_right().is_real_node()) and (not self.get_left().is_real_node())


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root = None
        self.min = AVLNode(9223372036854775807, None)

    """searches for a node in the dictionary corresponding to the key
    
    @type key: int
    @param key: a key to be searched
    @rtype: AVLNode
    @returns: node corresponding to key.
    """
    def search(self, key):
        curr = self.root
        if curr is None:
            return None
        while curr.is_real_node():
            curr_key = curr.get_key()
            if curr_key == key:
                return curr
            if curr_key > key:
                curr = curr.get_left()
            else:
                curr = curr.get_right()

        return None

    """inserts val at position i in the dictionary

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: any
    @param val: the value of the item
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """


    def insert(self, key, val):
        if self:
            node = AVLNode(key, val)
            return self.insert_node(node)

    def insert_node(self, node):
        if self.min.get_key() > node.get_key():
            self.min = node

        old_height = self.insert_bts(node)

        curr = node.get_parent()
        cnt = 0
        while curr is not None:
            if curr is not node.get_parent():
                old_height = curr.get_height()
            curr.update_fields()
            curr_BF = curr.get_BF()

            if abs(curr_BF) < 2 and old_height == curr.get_height():
                curr = curr.get_parent()
                continue
            if abs(curr_BF) < 2 and old_height != curr.get_height():
                cnt += 1
                curr = curr.get_parent()
                continue
            if abs(curr_BF) == 2:
                root = curr
                curr = root.get_parent()
                cnt += self.rotate(root, curr_BF)
                continue
        return cnt  # return the number of rebalancing operation due to AVL rebalancing

    def rotate(self, node, node_BF):
        left_BF = node.get_left().get_BF()
        right_BF = node.get_right().get_BF()
        if node_BF == 2:
            if left_BF == 1 or left_BF == 0:
                self.right_rotation(node)
                return 1
            if left_BF == -1:
                self.left_rotation(node.get_left())
                self.right_rotation(node)
                return 2
        elif node_BF == -2:
            if right_BF == 1:
                self.right_rotation(node.get_right())
                self.left_rotation(node)
                return 2
            if right_BF == -1 or right_BF == 0:
                self.left_rotation(node)
                return 1
        return 0

    def right_rotation(self, node):

        node_left = node.get_left()
        node_parent = node.get_parent()

        node.set_left(node_left.get_right())
        node.update_fields()
        node_left.set_right(node)
        node_left.update_fields()

        if node_parent is None:
            node_left.set_parent(None)
            self.root = node_left
        else:
            node_is_right_child = node_parent.is_right_child(node)
            if node_is_right_child:
                node_parent.set_right(node_left)
            else:
                node_parent.set_left(node_left)
            return None

    def left_rotation(self, node):

        node_right = node.get_right()
        node_parent = node.get_parent()

        node.set_right(node_right.get_left())
        node.update_fields()
        node_right.set_left(node)
        node_right.update_fields()

        if node_parent is None:
            node_right.set_parent(None)
            self.root = node_right
        else:
            node_is_right_child = node_parent.is_right_child(node)
            if node_is_right_child:
                node_parent.set_right(node_right)
            else:
                node_parent.set_left(node_right)
            return None

    # returns node parent old hight
    def insert_bts(self, node):
        if not AVLNode.is_real_node(self.get_root()):
            self.root = node
            return -2
        curr = self.get_root()
        my_side = None  # False -> im left child,else im right child
        temp = curr
        while curr.is_real_node():
            temp = curr.get_parent()

            if node.get_key() < curr.get_key():
                temp = curr
                curr = curr.get_left()
                my_side = False
            else:
                temp = curr
                curr = curr.get_right()
                my_side = True
        curr = temp
        parent_old_height = curr.get_height()
        if my_side is True:
            curr.set_right(node)
        else:
            curr.set_left(node)
        return parent_old_height

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, node):
        # update min
        if node is self.min:
            new_min = self.successor(node)
            if new_min is None: new_min = AVLNode(9223372036854775807, None)
            self.min = new_min

        y, old_height = self.delete_bts(node)
        # here y is the parent of the physically deleted node, or the parent of the parent of the physically deleted node
        cnt = 0  # rebalancing operations counter
        while y is not None:
            y.update_fields()
            y_BF = y.get_BF()
            if abs(y_BF) < 2 and (y.get_height() == old_height):
                y = y.get_parent()
                continue
            elif abs(y_BF) < 2 and (y.get_height() != old_height):
                y = y.get_parent()
                old_height = y.get_height() if y is not None else -2
                cnt += 1
                continue
            elif abs(y_BF) == 2:
                temp = y
                y = y.get_parent()
                old_height = y.get_height() if y is not None else -2
                cnt += self.rotate(temp, y_BF)
                continue

        return cnt

    # delete a node from bst tree. (without balancing)
    # returns the physically deleted node's parent and it's old_height
    def delete_bts(self, node):

        if node is None: return (None, -2)
        if not node.is_real_node(): return (None, -2)
        if node.is_leaf():
            return self.delete_case_1(node)

        elif not node.left.is_real_node():
            return self.delete_case_2(node)

        elif not node.right.is_real_node():
            return self.delete_case_2(node)

        else:  # has right and hase left
            return self.delete_case_3(node)

    # assume node is real leaf node,
    # returns deleted node and it's parent_old_height
    def delete_case_1(self, node):
        if self.get_root() is node:
            self.root = None
            AVLNode(9223372036854775807, None)
            return (None, -2)

        parent_old_height = node.get_parent().get_height()
        parent = node.get_parent()
        if parent.get_key() < node.get_key():
            parent.set_right(AVLNode(None, None))
        elif parent.get_key() > node.get_key():
            parent.set_left(AVLNode(None, None))

        node.set_parent(None)
        node.update_fields()
        parent.update_fields()
        return (parent, parent_old_height)

    # assume node hase just one child,
    # returns deleted node and it's parent_old_height
    def delete_case_2(self, node):
        if self.get_root() is node:
            if node.get_right().is_real_node():
                self.root = node.get_right()
            else:  # node.get_left().is_real_node()
                self.root = node.get_left()

        # update pointers
        parent = node.get_parent()
        if parent is None:
            # node is the root of self
            self.root.parent = None
            parent_old_height = -2
        else:
            parent_old_height = node.get_parent().get_height()
            if parent.get_right() is node:  # node is a right child (case2_Right)
                if node.get_right().is_real_node():
                    parent.set_right(node.get_right())
                    node.set_right(AVLNode(None, None))
                else:  # node.get_left().is_real_node()
                    parent.set_right(node.get_left())
                    node.set_left(AVLNode(None, None))

            else:  # node is a left child (case2_Left)
                if node.get_right().is_real_node():
                    parent.set_left(node.get_right())
                    node.set_right(AVLNode(None, None))
                else:  # node.get_left().is_real_node()
                    parent.set_left(node.get_left())
                    node.set_left(AVLNode(None, None))

        node.set_parent(None)
        return (parent, parent_old_height)

    # assume node hase 2 childs and not the root,
    # returns deleted successor and it's parent_old_height
    def delete_case_3(self, node):
        succ = self.successor(node)
        # observation: succ hase no left child
        # observation: succ have parent (he is not the root)
        # observation: succ exists (real node)

        # succ parent and height
        succ_old_height = succ.get_height()
        succ_parent_old_height = succ.get_parent().get_height()
        succ_parent = succ.get_parent()
        check_succ = False
        if succ_parent is node:
            check_succ = True
            succ_parent = node.get_parent()
        if succ.is_leaf():
            self.delete_case_1(succ)
        else:
            self.delete_case_2(succ)

        # replace node and succ
        if node.get_parent() is None:
            succ.set_parent(None)
            succ_parent_old_height = -2
        elif node.get_parent().get_key() < succ.get_key():
            node.get_parent().set_right(succ)
        else:
            node.get_parent().set_left(succ)
        succ.set_left(node.get_left())
        succ.set_right(node.get_right())
        if self.get_root() is node:
            self.root = succ
        node.set_parent(None)
        node.set_right(AVLNode(None, None))
        node.set_left(AVLNode(None, None))

        if check_succ:
            return (succ, succ_old_height)
        else:
            return (succ_parent, succ_parent_old_height)


    def successor(self, node):
        if node.has_right_child():
            curr = node.get_right()
            while curr.get_left().is_real_node():
                curr = curr.get_left()
            return curr
        else:
            curr = node
            while (curr.get_parent() is not None) and (curr.get_parent().is_right_child(curr)):
                curr = curr.get_parent()
        return curr.get_parent()

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """
    # takes an AVLTree tree and returns the minimum node in the tree
    def min_in_tree(self):
        curr = self.root
        if curr is None:
            return AVLNode(9223372036854775807, None)
        while curr.get_left().is_real_node():
            curr = curr.get_left()
        return curr


    def avl_to_array(self):
        if self.root is None:
            return []
        length = self.size()
        array = [None] * length
        curr = self.min_in_tree()
        for i in range(length):
            array[i] = (curr.get_key(), curr.get_value())
            curr = self.successor(curr)
        return array

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        if self.get_root() is None:
            return 0
        return self.get_root().get_size()

    """splits the dictionary at a given node

    @type node: AVLNode
    @pre: node is in self
    @param node: The intended node in the dictionary according to whom we split
    @rtype: list
    @returns: a list [left, right], where left is an AVLTree representing the keys in the 
    dictionary smaller than node.key, right is an AVLTree representing the keys in the 
    dictionary larger than node.key.
    """

    def split(self, node):  # TODO: may stuck in infinite loop!!!
        # initializing the new trees
        min_tree, max_tree = AVLTree(), AVLTree()
        max_tree.root = node.get_right()
        min_tree.root = node.get_left()
        AVLNode.set_parent(min_tree.root, None)
        AVLNode.set_parent(max_tree.root, None)

        # start joining
        curr = node.get_parent()
        while curr is not None:
            curr_parent = curr.get_parent()
            if curr is curr_parent:
                print("SPLIT: infinit loop detected!")
                break
            if curr.get_key() < node.get_key():
                # join to min_tree
                temp_min = AVLTree()
                temp_min.root = curr.get_left()
                temp_min.root.parent = None
                curr.set_right(AVLNode(None, None))
                curr.set_left(AVLNode(None, None))
                min_tree.join_node(temp_min, curr)
                AVLNode.update_size(min_tree.root)
            else:
                # join to max_tree
                temp_max = AVLTree()
                temp_max.root = curr.get_right()
                temp_max.root.parent = None
                curr.set_right(AVLNode(None, None))
                curr.set_left(AVLNode(None, None))
                max_tree.join_node(temp_max, curr)
                AVLNode.update_size(max_tree.root)


            curr = curr_parent

        if not AVLNode.is_real_node(min_tree.root):
            min_tree = AVLTree()
        if not AVLNode.is_real_node(max_tree.root):
            max_tree = AVLTree()
        AVLNode.set_parent(min_tree.root, None)
        AVLNode.set_parent(max_tree.root, None)

        min_tree.min = min_tree.min_in_tree()
        max_tree.min = max_tree.min_in_tree()
        return [min_tree, max_tree]

    """joins self with key and another AVLTree

    @type tree: AVLTree 
    @param tree: a dictionary to be joined with self
    @type key: int 
    @param key: The key separating self with tree
    @type val: any 
    @param val: The value attached to key
    @pre: all keys in self are smaller than key and all keys in tree are larger than key,
    or the other way around.
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def join(self, tree, key, val):

        node = AVLNode(key, val)
        return self.join_node(tree, node)

    def join_node(self, tree, node):
        # Extreme case: both trees are empty

        if not AVLNode.is_real_node(self.root) and not AVLNode.is_real_node(tree.root):
            self.insert(node.get_key(), node.get_value())
            self.min = node
            return 0
        # Extreme case: self is empty
        if not AVLNode.is_real_node(self.root):
            res = tree.get_root().get_height()
            tree.insert(node.get_key(), node.get_value())
            self.root = tree.root
            self.min = tree.min
            return res
        # Extreme case: tree is empty
        if not AVLNode.is_real_node(tree.root):
            res = self.get_root().get_height()
            self.insert(node.get_key(), node.get_value())
            return res

        # both trees are not empty

        self.root.parent = None
        tree.root.parent = None
        if self.root.get_key() < node.get_key():
            LT = self
            RT = tree
        else:
            LT = tree
            RT = self

        self.min = LT.min

        # (1) joining non empty trees
        h_LT = LT.get_root().get_height()
        h_RT = RT.get_root().get_height()
        if h_RT >= h_LT:
            # set left and right
            node.set_left(LT.get_root())
            h = h_LT
            curr = RT.get_root()  # from 1
            while abs(curr.get_height() - h) > 1:
                curr = curr.get_left()
            c = curr.get_parent()
            node.set_right(curr)

            # set parent
            if c is None:  # if true, then no rabalancing needed.
                self.root = node
                return abs(h_RT - h_LT)
            else:
                c.set_left(node)

        else:  # h_RT < h_LT
            # set left and right
            node.set_right(RT.get_root())
            h = h_RT
            curr = LT.get_root()
            while abs(curr.get_height() - h) > 1:
                curr = curr.get_right()
            c = curr.get_parent()
            node.set_left(curr)

            # set parent
            if c is None:  # if true, then no rabalancing needed.
                self.root = node
                return abs(h_RT - h_LT)
            else:
                c.set_right(node)

        # start rebalancing
        while curr is not None:
            curr.update_fields()
            curr_BF = curr.get_BF()
            curr.update_fields()
            if abs(curr_BF) == 2:
                temp = curr
                curr = curr.get_parent()
                self.rotate(temp, curr_BF)
                continue
            curr = curr.get_parent()
        # updating self root
        new_root = node
        while new_root.parent is not None:
            new_root = new_root.parent
        self.root = new_root
        AVLNode.set_parent(self.root, None)
        return abs(h_RT - h_LT)

    """compute the rank of node in the self

    @type node: AVLNode
    @pre: node is in self
    @param node: a node in the dictionary which we want to compute its rank
    @rtype: int
    @returns: the rank of node in self
    """

    def rank(self, node):
        rank_node = node.get_left().get_size() + 1
        curr = self.get_root()

        while curr is not node:

            if curr.get_key() < node.get_key():
                rank_node += curr.get_left().get_size() + 1
                curr = curr.get_right()
                continue
            curr = curr.get_left()

        return rank_node

    """finds the i'th smallest item (according to keys) in self

    @type i: int
    @pre: 1 <= i <= self.size()
    @param i: the rank to be selected in self
    @rtype: int
    @returns: the item of rank i in self
    """

    def select(self, i):
        if self.root is None:
            return None
        curr = self.get_root()
        while curr.is_real_node():
            cnt = curr.get_left().get_size() + 1  # num of nodes =< curr
            if cnt == i:
                return curr
            elif cnt < i:
                curr = curr.get_right()
                i = i - cnt
            elif cnt > i:
                curr = curr.get_left()

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return self.root



    def display(self, root):
        lines, *_ = self._display_aux(root)
        for line in lines:
            print(line)

    def _display_aux(self, node):
        if node is None:
            return '#'
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if not node.get_right() and not node.get_left():
            if not node.is_real_node():
                line = '%s' % "V"
            else:
                line = '%s' % node.get_key()

            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if not node.get_right() and node.get_left():
            lines, n, p, x = self._display_aux(node.get_left())
            s = '%s' % node.get_key()
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if not node.get_left() and node.get_right():
            lines, n, p, x = self._display_aux(node.get_right())
            s = '%s' % node.get_key()
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self._display_aux(node.get_left())
        right, m, q, y = self._display_aux(node.get_right())
        s = '%s' % node.get_key()
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2
