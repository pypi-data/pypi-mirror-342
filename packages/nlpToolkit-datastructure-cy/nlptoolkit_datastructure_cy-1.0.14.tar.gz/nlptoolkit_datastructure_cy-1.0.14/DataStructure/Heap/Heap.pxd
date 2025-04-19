cdef class Heap:

    cdef list __array
    cdef int __count
    cdef int __N
    cdef object comparator

    cpdef bint isEmpty(self)
    cpdef swapNode(self, int index1, int index2)
    cpdef percolateDown(self, int no)
    cpdef percolateUp(self, int no)
    cpdef object delete(self)
    cpdef insert(self, object data)
