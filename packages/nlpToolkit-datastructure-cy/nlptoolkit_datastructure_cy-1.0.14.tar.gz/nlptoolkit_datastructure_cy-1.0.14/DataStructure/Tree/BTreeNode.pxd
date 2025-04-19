cdef class BTreeNode:

    cdef list K
    cdef int m
    cdef int d
    cdef bint leaf
    cdef list children

    cpdef int position(self, object value, object comparator)
    cpdef insertIntoK(self, int index, object insertedK)
    cpdef moveHalfOfTheKToNewNode(self, BTreeNode newNode)
    cpdef moveHalfOfTheChildrenToNewNode(self, BTreeNode newNode)
    cpdef moveHalfOfTheElementsToNewNode(self, BTreeNode newNode)
    cpdef BTreeNode insertNode(self, object value, object comparator, bint isRoot)
    cpdef BTreeNode insertLeaf(self, object value, object comparator)
