from DataStructure.Tree.TreeNode cimport TreeNode

cdef class Tree:

    cdef TreeNode root
    cdef object comparator

    cpdef TreeNode search(self, object value)
    cpdef insertChild(self, TreeNode parent, TreeNode child)
    cpdef insert(self, TreeNode node)
    cpdef insertData(self, object data)
