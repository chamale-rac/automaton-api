class ThreeNode:
    '''
    Node of a tree

    :param data: (token, type)
    :param children: list of children
    :param id: unique id of the node
    '''

    def __init__(self, data: tuple[str, str], children: list = [], id=None):

        self.data = data  # (token, type)
        self.children = children
        self.id = id

    def deepcopy(self):
        '''
        Deepcopy the node

        :return: a deepcopy of the node
        '''
        return ThreeNode(self.data, [child.deepcopy() for child in self.children], self.id)
