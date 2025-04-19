cdef class HeapNode:

    def __init__(self, data: object):
        """
        Constructor of HeapNode.
        :param data: Data to be stored in the heap node.
        """
        self.__data = data

    cpdef object getData(self):
        """
        Mutator of the data field
        :return: Data
        """
        return self.__data

    def __repr__(self):
        return f"{self.__data}"
