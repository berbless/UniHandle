"""Hash Table"""

import numpy as np

class DSAHashTable:
    """Hash Table"""
    # Hash data
    __hash_array = None
    # count of items
    __length = 0
    # max items can currently hold
    __max = 0
    # threshold
    __max_threshold = 0.7
    __min_threshold = 0.3
    # resize AAA
    __do_resize = True

    # only way I could think to make it private
    class _DSAHashEntry:
        """Hash Node"""
        __value = None
        __hask = None
        __key = None

        def __init__(self, key, hask, value):
            self.__hask = hask
            self.__value = value
            self.__key = key

        # if the hask matches the stored, return the data
        # else give nothing
        def get(self, hask):
            """hask | Return the value"""
            if hask == self.__hask:
                return self.__value
            else:
                return None

        def key(self, hask):
            # return the key if the correct key
            """Return key"""
            if hask == self.__hask:
                return self.__key

        def dump(self):
            """Shh, its a secret."""
            return (self.__key, self.__value)

    class Empty:
        """Nething borgar"""
        def key(self, hask):
            """Return None"""
            return ""

    def __init__(self, size = 3):
        # set the max length
        self.__max = size
        # resize to nearest prime
        self.__max = self.get_closest_prime(self.__max)
        # set the array
        self.__hash_array = np.empty(self.__max, dtype=object)

    def __hash(self, key_value):
        """key | hash the key"""
        hash_index = 0
        # for each text char
        for char in key_value:
            # shift by mul 33 then add the chars value
            hash_index = (33 * hash_index) + ord(char)
        # Loop it back into the length of the array
        return hash_index % self.__max

    def __move(self, hask):
        return (hask + 1) % self.__max

    def get_load(self):
        """Return the load factor."""
        return self.__length / self.__max


    def is_prime(self, integer):
        """integer | returns if the integer is a prime."""
        if isinstance(integer, str) and integer.isnumeric():
            num = int(integer)
        else:
            num = integer

        itterable = 2
        is_prime = True

        # go through base nums, check against
        while itterable <= 10 and is_prime:
            is_prime = (itterable == num) or (num % itterable != 0)
            itterable += 1
        return is_prime

    def get_closest_prime(self, integer):
        """integer | returns the next prime up from the integer."""
        if isinstance(integer, str) and integer.isnumeric():
            num = int(integer)
        else:
            num = integer

        # while not at a prime
        while not self.is_prime(num):
            # itterate up
            num += 1
        return num

    def __resize(self):
        """Re-hash all values into a larger table"""
        load_factor = 0

        if self.__length > 0:
            # LF = __length / len(__hash_array)
            load_factor = self.__length / self.__max
            if load_factor > self.__max_threshold:
                self.__refresh_up()
            if load_factor < self.__min_threshold:
                self.__refresh_down()

    def __refresh_up(self):
        # divide the length by threshold to get what 60% would look like
        new_max = int((self.__max_threshold * self.__max))
        # set the max value
        new_max += self.__max
        # convert to the closest prime
        new_max = self.get_closest_prime(new_max)
        # resize to new max
        self.__refresh_table(new_max)

    def __refresh_down(self):
        # divide the length by threshold to get what 60% would look like
        new_max = int((self.__max / 2))
        # convert to the closest prime
        new_max = self.get_closest_prime(new_max)
        # resize to new max
        self.__refresh_table(new_max)

    def __refresh_table(self, new_max):
        # get the old values
        old_table = self.__hash_array

        # make a new table of a bigger length
        self.__hash_array = np.empty(new_max, dtype=object)
        # set the array max to new
        self.__max = new_max
        # reset length
        self.__length = 0

        # loop over array
        itterable = 0
        self.__do_resize = False
        while itterable < old_table.size:
            # get an item from the old table
            item = old_table[itterable]
            # if it is an item
            if isinstance(item, self._DSAHashEntry):
                # dump the values
                val = item.dump()
                # add the data back in a new hash
                self.put(val[0], val[1])
            itterable += 1
        self.__do_resize = True
        itterable = 0

    def put(self, key, value):
        """key, value | put the value into the hash table with key"""
        # hash the key
        hask = self.__get_empty(key)

        # if not already included
        if hask is not None:
            # set the thing in the spot
            self.__hash_array[hask] = self._DSAHashEntry(key, hask, value)
            self.__length += 1
            # rebalance if needs be
            if self.__do_resize:
                self.__resize()
            # self.__print_array()
        else:
            print(f"{key} Something is very wrong.")

    def delete(self, key):
        """key | Remove the value at key"""
        hask = self.__has_key(key)
        print(f"{key} - {hask}")

        # attempt an item get
        if hask is not None:
            # Set the value to None
            self.__hash_array[hask] = self.Empty()
            self.__length -= 1
            # rebalance if needs be
            if self.__do_resize:
                self.__resize()
            # self.__print_array()
        else:
            print(f"{key} not in the hash table.")

    def get(self, key):
        """key | get a value stored at key"""
        hask = self.__has_key(key)
        item = None

        # attempt an item get
        if hask is not None:
            item = self.__hash_array[hask]
            print(item.key(hask))
            print(item.get(hask))
        else:
            print(f"{key} not in the hash table.")

        # return
        return item

    def __has_key(self, key):
        """Does this key exist in the table?, returns the hash"""
        # hash the key
        hask_original = self.__hash(key)
        hask = hask_original

        found = False
        give_up = False

        while not (found or give_up):
            # get first
            item = self.__hash_array[hask]

            # if reached end
            if item is None:
                give_up = True
            # if found
            elif not isinstance(item, self.Empty) and item.key(hask) == key:
                found = True
            # if none, move along
            else:
                hask = self.__move(hask)
                # if made full loop, give up
                if hask == hask_original:
                    give_up = True

        # if not found, blank out wrong or already None key
        if give_up:
            hask = None

        return hask

    def __get_empty(self, key):
        """Does this key exist in the table?, returns the hash"""
        # hash the key
        hask_original = self.__hash(key)
        hask = hask_original

        found = False
        give_up = False

        while not (found or give_up):
            if self.__hash_array[hask] is None:
                found = True
            else:
                hask = self.__move(hask)
        return hask

    def has_key(self, key):
        """key | does this key exist in the table?"""
        return self.__has_key(key) is not None

    def __print_array(self):
        itterable = 0
        count = 0
        print("")
        while itterable < self.__max:
            if isinstance(self.__hash_array[itterable], self.Empty):
                print(f"[{itterable}] Empty")
            elif self.__hash_array[itterable] is not None:
                print(f"[{itterable}] {self.__hash_array[itterable].dump()}")
                count += 1
            else:
                print(f"[{itterable}] None")
            itterable += 1
        print(f"Count: {count} | Length {self.__max} | {self.get_load()}")

    def load_csv(self, file_name):
        """file_name | open the file, load the csv."""
        # itterable for reporting line errors.
        itterable = 0

        with open(file_name, "r") as file:
            for line in file.readlines():
                itterable += 1
                if len(line.split(",")) != 2:
                    # the line does not have just a key value pair.abs
                    print(f"Error on line {itterable}: Not correct amount of entries")
                    print("Needs: 2 (key,value)")
                    print(f"Given: {len(line.split(","))} ({line})")
                else:
                    # try to add the data
                    line = line.strip("\n")
                    print(f"Attempting Add {itterable}: ({line})")
                    self.put(line.split(",")[0], line.split(",")[1])
