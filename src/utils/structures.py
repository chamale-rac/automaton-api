class ThreeNode:
    def __init__(self, data, children=[], id=None):
        self.data = data
        self.children = children
        self.id = id

    def deepcopy(self):
        '''
        Deepcopy the node

        :return: a deepcopy of the node
        '''
        return ThreeNode(self.data, [child.deepcopy() for child in self.children], self.id)
