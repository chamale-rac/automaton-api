from graphviz import Digraph
from .utils.structures import ThreeNode
from .expression import Expression


class NonDeterministicFiniteAutomaton:
    def __init__(self, ast: ThreeNode, alphabet: set[tuple[str, str]]) -> None:
        self.ast = ast.deepcopy()
        self.alphabet = alphabet
        # (id_initial, id_alphabet: (toke, type), id_final)
        self.transitions: list[tuple[int, tuple[str, str], int]] = []
        self.graph = None
        self.id_initial = None
        self.id_final = None

    def thompson(self):
        '''
        Convert the abstract syntax tree to a non-deterministic finite automaton
        '''
        id_global = 0

        def compose(ast: ThreeNode):
            nonlocal id_global
            if ast.data[1] in ['escaped', 'character']:
                id_initial, id_final = range(id_global, id_global + 2)
                id_global += 2

                self.transitions.append((id_initial, ast.data, id_final))
                return id_initial, id_final
            elif ast.data[1] == 'operator':
                match ast.data[0]:
                    case '•':
                        l_id_initial, l_id_final = compose(ast.children[1])
                        id_global -= 1
                        r_id_initial, r_id_final = compose(ast.children[0])

                        return l_id_initial, r_id_final
                    case '|':
                        id_initial = id_global
                        id_global += 1

                        l_id_initial, l_id_final = compose(ast.children[1])
                        r_id_initial, r_id_final = compose(ast.children[0])

                        id_final = id_global
                        id_global += 1

                        self.transitions.append(
                            (id_initial, ('ϵ', 'character'), l_id_initial))
                        self.transitions.append(
                            (id_initial, ('ϵ', 'character'), r_id_initial))

                        self.transitions.append(
                            (l_id_final, ('ϵ', 'character'), id_final))
                        self.transitions.append(
                            (r_id_final, ('ϵ', 'character'), id_final))

                        return id_initial, id_final
                    case '*':
                        id_initial = id_global
                        id_global += 1

                        c_id_initial, c_id_final = compose(
                            ast.children[0])  # UNIQUE CHILD

                        id_final = id_global
                        id_global += 1

                        self.transitions.append(
                            (id_initial, ('ϵ', 'character'), c_id_initial))
                        self.transitions.append(
                            (id_initial, ('ϵ', 'character'), id_final))

                        self.transitions.append(
                            (c_id_final, ('ϵ', 'character'), c_id_initial))
                        self.transitions.append(
                            (c_id_final, ('ϵ', 'character'), id_final))

                        return id_initial, id_final

        self.id_initial, self.id_final = compose(self.ast)

    def rasterize(self, web=False):
        '''
        Render the NFA to a graphviz 
        '''
        if web:
            label = None
        else:
            label = f'Non deterministic finite automaton'

        attributes = {
            'rankdir': 'LR',
            'label': label,
            'labelloc': 'b',
            'fontname': 'Helvetica'
        }

        digraph = Digraph(graph_attr=attributes)

        digraph.node('start', 'start', shape='none')
        digraph.node(str(self.id_initial), str(self.id_initial))
        digraph.node(str(self.id_final), str(
            self.id_final), shape='doublecircle')

        digraph.edge('start', str(self.id_initial))

        def compose(transitions):
            for transition in transitions:
                # transitions: (id_initial, id_alphabet: (token, type), id_final)
                digraph.node(str(transition[0]), str(transition[0]))
                digraph.node(str(transition[2]), str(transition[2]))
                digraph.edge(str(transition[0]), str(
                    transition[2]), str(transition[1][0]))

        compose(self.transitions)

        self.graph = digraph

    def e_closure(self, id):
        '''
        Get the epsilon closure of a state

        :param id: state id
        :return: a set of states
        '''
        closure = set()

        def e_closure_intern(id):
            if id not in closure:
                closure.add(id)
                for i, token, j in self.transitions:
                    if i == id and token == ('ϵ', 'character'):
                        e_closure_intern(j)

        e_closure_intern(id)
        return closure

    def move(self, id, token):
        '''
        Get the move of a state with a char token
        '''
        return {any for i_, token_, any in self.transitions if i_ == id and token_ == token}

    def simulate(self, string: str):
        '''
        Simulate the NFA with a string
        '''
        expression = Expression(string)
        expression.format()
        expression.format_string()

        closure = self.e_closure(self.id_initial)
        for token in expression.formatted:
            matched_nodes = set()
            for id in closure:
                any_values = self.move(id, token)
                if any_values:
                    matched_nodes.update(any_values)
            if len(matched_nodes) == 0:
                return False
            closure = set()
            for id in matched_nodes:
                closure.update(self.e_closure(id))
        for id in closure:
            if id == self.id_final:
                return True
        else:
            return False
