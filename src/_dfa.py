from graphviz import Digraph
from ._nfa import NonDeterministicFiniteAutomaton
from .utils.tools import get_letter


class DeterministicFiniteAutomaton:
    def __init__(self, nfa: NonDeterministicFiniteAutomaton, alphabet: set[tuple[str, str]]) -> None:
        self.nfa_transitions = nfa.transitions
        self.nfa_id_initial: int = nfa.id_initial
        self.nfa_id_final: int = nfa.id_final

        self.alphabet = sorted(alphabet, key=lambda x: ord(str(x[0])))
        self.alphabet.append(('ε*', 'character'))

        self.subsets_first = None
        self.transition_table = None
        self.states = None

        self.graph = None

    def eClosure(self, id):
        '''
        Get the epsilon closure of a state

        :param id: state id
        :return: a set of states
        '''
        closure = set()

        def eClosureIntern(id):
            if id not in closure:
                closure.add(id)
                for i, token, j in self.nfa_transitions:
                    if i == id and token == ('ε', 'character'):
                        eClosureIntern(j)

        eClosureIntern(id)
        return closure

    def subsetsBuild(self) -> None:
        '''
        Build the deterministic finite automaton from the non-deterministic finite automaton
        '''
        subsets_first = []

        for i in range(self.nfa_id_final+1):
            row = []
            for token in self.alphabet[:-1]:
                any_values = {
                    any for i_, token_, any in self.nfa_transitions if i_ == i and token_ == token}
                row.append(any_values)
            row.append(self.eClosure(i))
            subsets_first.append(row)

        self.subsets_first = subsets_first

        transition_table = []
        dfa_states = []
        dfa_states.append(subsets_first[self.nfa_id_initial][-1])

        for i, dfa_state in enumerate(dfa_states):
            row = [(get_letter(i), bool(self.nfa_id_final in dfa_state))]
            for token_index in range(len(self.alphabet)-1):
                vals = []
                for nfa_state in dfa_state:
                    vals.extend(subsets_first[nfa_state][token_index])
                vals = set(vals)
                e_closure_vals = []
                for val in vals:
                    e_closure_vals.extend(subsets_first[val][-1])
                e_closure_vals = set(e_closure_vals)

                if e_closure_vals not in dfa_states:
                    dfa_states.append(e_closure_vals)
                letter = get_letter(dfa_states.index(e_closure_vals))
                row.append(letter)
            transition_table.append(row)

        self.states = dfa_states
        self.transition_table = transition_table

    def rasterize(self, web=False):
        '''
        Render the NFA to a graphviz 
        '''
        if web:
            label = None
        else:
            label = f'Deterministic finite automaton'

        attributes = {
            'rankdir': 'LR',
            'label': label,
            'labelloc': 'b',
            'fontname': 'Helvetica',
        }

        digraph = Digraph(graph_attr=attributes)

        digraph.node('start', 'start', shape='none')
        digraph.edge('start', 'A')

        def compose(transition_table):
            for row in transition_table:
                for i, state in enumerate(row[1:]):
                    digraph.edge(row[0][0], state, self.alphabet[i][0])
                if row[0][1]:
                    digraph.node(row[0][0], row[0][0], shape='doublecircle')

        compose(self.transition_table)

        self.graph = digraph
