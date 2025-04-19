cdef class AvlTreeNode(TreeNode):

    def __init__(self, data: object):
        super().__init__(data)
        self.height = 1
