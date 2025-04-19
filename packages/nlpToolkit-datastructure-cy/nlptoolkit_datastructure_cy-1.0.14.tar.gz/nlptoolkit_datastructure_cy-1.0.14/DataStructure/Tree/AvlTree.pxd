from DataStructure.Tree.AvlTreeNode cimport AvlTreeNode
from DataStructure.Tree.Tree cimport Tree
from DataStructure.Tree.TreeNode cimport TreeNode

cdef class AvlTree(Tree):

    cpdef int height(self, AvlTreeNode d)
    cpdef AvlTreeNode rotateLeft(self, AvlTreeNode k2)
    cpdef AvlTreeNode rotateRight(self, AvlTreeNode k1)
    cpdef doubleRotateLeft(self, AvlTreeNode k3)
    cpdef doubleRotateRight(self, AvlTreeNode k1)
    cpdef insertTree(self, AvlTreeNode node)
    cpdef insertData(self, object data)
