from graphviz import Digraph
from .utils.structures import ThreeNode as tn


class AbstractSyntaxTree:
    def __init__(self, expression):
        self.expression = expression
        self.builded = None
        self.graph = None

    def serialize(self):
        '''
        Serialize the abstract syntax tree assigning a unique id to each node

        :return: builded but with the id assigned
        '''
        _id_global = 0

        def compose(three_node):
            nonlocal _id_global
            three_node.id = _id_global
            _id_global += 1
            for child in three_node.children:
                compose(child)

            return three_node

        compose(self.builded)

    def build(self):
        '''
        Build the abstract syntax tree from the postfix expression

        :return: a list of nodes
        '''
        stack = []

        for token in self.expression.postfix:
            if token[1] in ['grouping', 'escaped', 'character']:
                stack.append(tn(token))
            elif token[1] == 'operator':
                match token[0]:
                    case '*':
                        stack.append(tn(token, [stack.pop()]))
                    case '•':
                        stack.append(tn(token, [stack.pop(), stack.pop()]))
                    case '|':
                        stack.append(tn(token, [stack.pop(), stack.pop()]))
                    case '?':
                        stack.append(
                            tn(('|', 'operator'), [stack.pop(), tn(('ε', 'character'))]))
                    case '+':
                        peaked = stack.pop()
                        clean = tn(('*', 'operator'), [peaked])
                        stack.append(
                            tn(('•', 'operator'), [clean, peaked.deepcopy()]))
        self.builded = stack.pop()
        self.serialize()

    def rasterize(self):
        '''
        Render the abstract syntax tree to a graphviz 
        '''
        label = f'Abstract Syntax Tree\ninfix = {self.expression.infix} | postfix = {self.expression.postfix_string}'

        attributes = {
            'rankdir': 'TB',
            'label': label,
            'labelloc': 'b',
        }

        digraph = Digraph(graph_attr=attributes)

        def compose(three_node):
            digraph.node(str(three_node.id), str(three_node.data[0]))
            for child in reversed(three_node.children):
                compose(child)
                digraph.edge(str(three_node.id), str(child.id))
            return three_node

        compose(self.builded)

        self.graph = digraph
