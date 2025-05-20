"""TBDOCCED"""

class DSAListNodeDouble:
    """TBDOCCED"""
    __value = None
    __next = None
    __prev = None

    def __init__(self, value, next_node = None, prev_node = None):
        self.__value = value
        self.__next = next_node
        self.__prev = prev_node

    def get_value(self):
        """TBDOCCED"""
        return self.__value

    def set_value(self, value):
        """TBDOCCED"""
        self.__value = value

    def get_next(self):
        """TBDOCCED"""
        return self.__next

    def set_next(self, next_node):
        """TBDOCCED"""
        self.__next = next_node

    def get_prev(self):
        """TBDOCCED"""
        return self.__prev

    def set_prev(self, prev_node):
        """TBDOCCED"""
        self.__prev = prev_node

class DSALinkedListDouble:
    """TBDOCCED"""
    OUT_OF_RANGE = -1
    LIST_IS_EMPTY = -2
    __head = None
    __tail = None
    __count = 0

    def __init__(self, value=None):
        # Set a head if given
        if value is not None:
            __head = DSAListNodeDouble(value)

    def is_empty(self):
        """TBDOCCED"""
        # return if head is none
        return self.__head is None

    def length(self):
        """TBDOCCED"""
        return self.__count

    def __sizeof__(self):
        return self.length()

    def __get_at(self, index):
        next_node = None

        # do error checking (empty, or out of range)
        if self.length() <= index and index < 0 or (self.is_empty()):
            print(f"{index} is out of range of list")
        else:
            count = 0
            next_node = self.__head
            # while in list and before index (just in case)
            while count < index:
                count += 1
                # TODO Continue Here
                next_node.get_next()

        return next_node

    # def insert_at(self, index, value):
    #     """TBDOCCED"""
    #     # if not asking for first
    #     if index == 0:
    #         # return popped first
    #         self.insert_first(value)
    #     elif index == (self.__count - 1):
    #         # if last do opposite
    #         self.insert_last(value)
    #     else:
    #         # get the node at the index
    #         next_node = self.__get_at(index)
    #         if next_node is not None:
    #             # get last next
    #             old = next_node.get_next()
    #             # set the new node to next
    #             next_node.set_next(DSAListNodeDouble(value, old))
    #             # add one to count
    #             self.__count +=1

    def peek_at(self, index):
        """TBDOCCED"""
        # TODO AAA
        # if not asking for first
        if index == 0:
            # return popped first
            return self.peek_first()
        elif index == (self.__count - 1):
            # if last do opposite
            return self.peek_last()
        else:
            # return the value of the spot
            output = self.__get_at(index)
            # if not None, pull value
            if output is not None:
                output = output.get_value()
            return output

    def pop_at(self, index):
        """TBDOCCED"""
        # TODO AAAAAAAAAAAAAAA
        # if not asking for first
        if index == 0:
            # return popped first
            return self.pop_first()
        elif index == (self.__count - 1):
            # if last do opposite
            return self.pop_last()
        else:
            # get node before
            node = self.__get_at(index - 1)
            next_node = None
            # if the value isn't the last
            if node is not None and node.get_next() is not None:
                # get node to remove
                next_node = node.get_next()
                # set the previos nodes next to the next nodes next.
                node.set_next(next_node.get_next())
                # If there is at least one more node to the right
                if not node.get_next() is None:
                    # Set that nodes prev to not include the dropped
                    node.get_next().set_prev(node)
                else:
                    # Else, it must be at the end now.
                    self.__tail = node
                # decrement the node count
                self.__count -= 1

            # return value
            return next_node


    def __validate_custom(self, func):
        # Function Must:
        # Accept a Node
        # Proccess it individually (or with one extra either side at most)
        # Return a boolean value
        try:
            # if the function passes the tests, allow.
            is_valid = True
            if func.__code__.co_argcount < 1:
                is_valid = False
            else:
                # make a dummy list of two items
                dummy = DSALinkedListDouble()
                dummy.insert_first("a")
                dummy.insert_last("b")
                dummy.insert_last("c")
                # attempt to run the middle node through it
                output = func(dummy.peek_at(1))
                # If the return type isn't a bool
                if not isinstance(output, bool):
                    # invalid
                    is_valid = False
        # If it cannot handle the peram count (1)
        except TypeError:
            # It isn't going to work
            is_valid = False

        return is_valid

    def find_custom(self, function, skip_validation = False):
        """function | Find a node that matches the custom value"""
        # If not, itterate through
        node = None

        # if the custom function is correct (can handle running)
        if skip_validation or self.__validate_custom(function):
            node = self.__head

            # while neither at end OR
            while not node is None and not function(node):
                # get the next
                node = node.get_next()
        else:
            print("invalid filter function!")

        return node

    def find(self, value):
        """Find a node with value"""
        node = None

        # If empty
        if self.is_empty():
            print("List is empty")
        else:
            # If not, itterate through
            node = self.__head
            # check that
            self.find_custom(lambda node: node.get_value() != value)

        return node



    def insert_first(self, value):
        """TBDOCCED"""
        # make a new node with head as next
        new = DSAListNodeDouble(value, next_node=self.__head)

        # set prev of old head if old head is not none
        if self.__head is not None:
            self.__head.set_prev(new)

        # set new node to head
        self.__head = new

        # if empty, tail is head
        if self.__count == 0:
            self.__tail = new

        # add one to the count
        self.__count += 1

    def insert_last(self, value):
        """TBDOCCED"""
        # make a new node with head as next
        new = DSAListNodeDouble(value, prev_node=self.__tail)

        # set next of old tail if old tail is not none
        if self.__tail is not None:
            self.__tail.set_next(new)

        # set new node to head
        self.__tail = new

        # if empty, head is tail
        if self.__count == 0:
            self.__head = new

        # add one to the count
        self.__count += 1

    def get_first(self):
        """TBDOCCED"""
        output = self.__head
        if output is not None:
            output = output
        return output

    def peek_first(self):
        """TBDOCCED"""
        out = self.get_first()
        if out is not None:
            out = out.get_value()
        return out

    def get_last(self):
        """TBDOCCED"""
        output = self.__tail
        if output is not None:
            output = output
        return output

    def peek_last(self):
        """TBDOCCED"""
        out = self.get_last()
        if out is not None:
            out = out.get_value()
        return out

    def pop_first(self):
        """TBDOCCED"""
        # if not empty
        if self.is_empty():
            print("List is empty")
        else:
            old = self.__head
            # get next to head
            next_node = self.__head.get_next()
            # set as head
            self.__head = next_node
            self.__count -= 1

            # if head is not none, set the prev to it to None
            if self.__head is not None:
                self.__head.set_prev(None)

            # return last head
            if old is not None:
                old = old.get_value()
            return old

    def pop_last(self):
        """TBDOCCED"""
        # if not empty
        if self.is_empty():
            print("List is empty")
        else:
            old = self.__tail
            # get next to head
            prev = self.__tail.get_prev()
            # set as head
            self.__tail = prev
            self.__count -= 1

            # if tails is not none, set the next to it to None
            if self.__tail is not None:
                self.__tail.set_next(None)

            # return last head
            if old is not None:
                old = old.get_value()
            return old
