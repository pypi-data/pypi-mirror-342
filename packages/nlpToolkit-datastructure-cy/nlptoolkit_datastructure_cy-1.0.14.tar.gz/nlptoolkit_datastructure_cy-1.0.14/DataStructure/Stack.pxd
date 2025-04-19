cdef class Stack:

    cdef list __stack

    cpdef push(self, object item)
    cpdef object pop(self)
    cpdef bint isEmpty(self)
