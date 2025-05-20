from DSAListDouble import DSALinkedListDouble
import sys

class DSAStack:
    # Data store
    __list = None

    # Current count of elements
    __current_count = 0

    def __init__(self):
        # Set dimentions of array
        self.__list = DSALinkedListDouble() 

    def is_empty(self):
        # Return if the stack is empty
        return (self.__current_count < 1)

    def __str__(self):
            node = self.__list.get_first()
            output = ""
            while node is not None:
                output += node.get_value() + ", "
                node = node.get_next()
            return output

    def count(self):
        # return current count
        return self.__current_count

    def __len__(self):
        return self.__current_count

    def top(self):
        top_val = None
        if not self.is_empty():
            # return top value
            top_val = self.__list.peek_last()
        return top_val

    def push(self, value):
        # If there is room
        # Add it to the next
        self.__list.insert_last(value)
        self.__current_count += 1

    def pop(self):
        pop_val = None
        # If there is values
        if not self.is_empty():
            self.__current_count -= 1
            # output last top
            pop_val = self.__list.pop_last()
        return pop_val