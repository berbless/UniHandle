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
    __itterable_head = None

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

    def __len__(self):
        return self.__count

    def __sizeof__(self):
        return self.length()

    # 21/05/25 - 6:20pm https://www.w3schools.com/python/python_iterators.asp
    def __iter__(self):
        self.__itterable_head = self.__head
        return self

    # 21/05/25 - 6:20pm https://www.w3schools.com/python/python_iterators.asp
    def __next__(self):
        current = None
        # if not still in array
        if self.__itterable_head is not None:
            # get current
            current = self.__itterable_head
            # itterate to the next item
            self.__itterable_head = self.__itterable_head.get_next()
            # return current.
            return current.get_value()
        else:
            # raise, end of itteration
            raise StopIteration

    # used for converting argv into a constructed list
    def import_list(self, argv):
        """Import the sys args to non in-built, as it comes through as a default list."""
        for item in argv:
            self.insert_last(item)

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
        return self.__head

    def peek_first(self):
        """TBDOCCED"""
        out = self.get_first()
        if out is not None:
            out = out.get_value()
        return out

    def get_last(self):
        """TBDOCCED"""
        return self.__tail

    def peek_last(self):
        """TBDOCCED"""
        out = self.get_last()
        if out is not None:
            out = out.get_value()
        return out

    def pop_first(self):
        """TBDOCCED"""
        output = None
        # if not empty
        if not self.is_empty():
            output = self.__head
            # get next to head
            next_node = self.__head.get_next()
            # set as head
            self.__head = next_node
            self.__count -= 1

            # if head is not none, set the prev to it to None
            if self.__head is not None:
                self.__head.set_prev(None)

            # return last head
            if output is not None:
                output = output.get_value()
        return output

    def pop_last(self):
        """TBDOCCED"""
        output = None
        # if not empty
        if not self.is_empty():
            output = self.__tail
            # get next to head
            prev = self.__tail.get_prev()
            # set as head
            self.__tail = prev
            self.__count -= 1

            # if tails is not none, set the next to it to None
            if self.__tail is not None:
                self.__tail.set_next(None)

            # return last head
            if output is not None:
                output = output.get_value()
        return output
