from DataStructure.Tree.TreeNode cimport TreeNode

cdef class AvlTreeNode(TreeNode):

    cdef int height
