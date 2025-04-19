from DataStructure.Tree.BTreeNode cimport BTreeNode

cdef class BTree:

    cdef BTreeNode root
    cdef object comparator
    cdef int d

    cpdef BTreeNode search(self, object value)
    cpdef insertData(self, object data)
