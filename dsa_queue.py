from dsa_double_list import DSALinkedListDouble
import sys

class DSAQueue:
    # Data store
    __list = None

    # Current count of elements
    __current_count = 0

    def __init__(self):
        # Set dimentions of array
        self.__list = DSALinkedListDouble()

    def __str__(self):
        node = self.__list.get_first()
        output = ""
        while node is not None:
            output += node.get_value() + " "
            node = node.get_next()
        return output

    def is_empty(self):
        # Return if the stack is empty
        return (self.__current_count == 0)

    def count(self):
        # return current count
        return self.__current_count + 1

    def __len__(self):
        return self.__current_count

    def peek(self):
        # if there is something to peek
        if not self.is_empty():
            # peek
            return self.__list.peek_first()

    def add(self, value):
        # Add it to the next
        self.__list.insert_last(value)
        self.__current_count += 1

    def pop(self):
        pop_val = None
        if not self.is_empty():
            # Get the top of the queue
            pop_val = self.__list.pop_first()
        return pop_val
