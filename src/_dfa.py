from graphviz import Digraph
from ._nfa import NonDeterministicFiniteAutomaton
from .utils.tools import get_letter


class DeterministicFiniteAutomaton:
    def __init__(self, nfa: NonDeterministicFiniteAutomaton, alphabet: set[tuple[str, str]]) -> None:
        self.nfa = nfa
        self.alphabet = sorted(alphabet, key=lambda x: ord(str(x[0])))
        self.alphabet.append(('ϵ*', 'character'))
        if ('ϵ', 'character') in self.alphabet:
            self.alphabet.remove(('ϵ', 'character'))

        self.subsets_first = None
        self.transition_table = None
        self.states = None

        self.graph = None

        self.min_transition_table = None
        self.min_transition_states = None
        self.min_graph = None
        self.accepting_states = None
        self.non_accepting_states = None

    def subsetsBuild(self) -> None:
        '''
        Build the deterministic finite automaton from the non-deterministic finite automaton
        '''
        subsets_first = []

        for i in range(self.nfa.id_final+1):
            row = []
            for token in self.alphabet[:-1]:
                any_values = self.nfa.move(i, token)
                row.append(any_values)
            row.append(self.nfa.e_closure(i))
            subsets_first.append(row)

        self.subsets_first = subsets_first

        transition_table = []
        dfa_states = []

        dfa_states.append(subsets_first[self.nfa.id_initial][-1])

        for i, dfa_state in enumerate(dfa_states):
            row = [(get_letter(i), bool(self.nfa.id_final in dfa_state))]
            for token_index in range(len(self.alphabet)-1):
                vals = []
                for nfa_state in dfa_state:
                    vals.extend(subsets_first[nfa_state][token_index])
                vals = set(vals)
                e_closure_vals = []
                for val in vals:
                    e_closure_vals.extend(subsets_first[val][-1])
                e_closure_vals = set(e_closure_vals)

                if e_closure_vals != set():
                    if e_closure_vals not in dfa_states:
                        dfa_states.append(e_closure_vals)
                    letter = get_letter(dfa_states.index(e_closure_vals))
                else:
                    letter = None

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
            'fontname': 'Helvetica'
        }

        digraph = Digraph(graph_attr=attributes)

        digraph.node('start', 'start', shape='none')
        digraph.edge('start', 'A')

        def compose(transition_table):
            for row in transition_table:
                for i, state in enumerate(row[1:]):
                    if state != None:
                        digraph.edge(row[0][0], state, self.alphabet[i][0])
                if row[0][1]:
                    digraph.node(row[0][0], row[0][0], shape='doublecircle')

        compose(self.transition_table)

        self.graph = digraph

    def minimize(self):
        '''
        Implementing the partition algorithm to minimize the DFA
        '''
        self.accepting_states = [get_letter(self.states.index(
            state)) for state in self.states if self.nfa.id_final in state]
        self.non_accepting_states = [get_letter(self.states.index(
            state)) for state in self.states if self.nfa.id_final not in state]

        partition = [self.accepting_states, self.non_accepting_states]

        def partition_algorithm(partition):
            partition_table = []
            for row in self.transition_table:
                combination = []
                for state in [row[0][0]]+list(row[1:]):
                    for i, part in enumerate(partition):
                        if state is None:
                            combination.append(None)
                            break
                        elif state in part:
                            combination.append(i)
                            break
                partition_table.append([row[0][0], tuple(combination)])

            partition_sets = []
            partitions_temp = []
            for row in partition_table:
                if row[1] not in partitions_temp:
                    partitions_temp.append(row[1])
                    partition_sets.append([row[0]])
                else:
                    partition_sets[partitions_temp.index(
                        row[1])].append(row[0])

            return partition_table, partition_sets

        while True:
            partition_table, partition_sets = partition_algorithm(partition)
            if partition_sets == partition:
                break
            partition = partition_sets

        self.min_transition_states = partition_sets
        self.min_transition_table = partition_table

    def min_rasterize(self, web=False):
        '''
        Render the NFA to a graphviz 
        '''
        if web:
            label = None
        else:
            label = f'Minimized deterministic finite automaton'

        attributes = {
            'rankdir': 'LR',
            'label': label,
            'labelloc': 'b',
            'fontname': 'Helvetica'
        }

        digraph = Digraph(graph_attr=attributes)

        def compose(transition_table, states):
            initial_states = [get_letter(self.states.index(
                state)) for state in self.states if self.nfa.id_initial in state]

            index_dict = {}
            for i, state in enumerate(states):
                for letter in state:
                    index_dict[letter] = i

            initial_id = str(index_dict[initial_states[0]])
            digraph.node('start', 'start', shape='none')
            digraph.node(initial_id, initial_id)
            digraph.edge('start', initial_id)

            curated_table = [transition_table[0]]
            for row in transition_table:
                if row[1] not in [combination for _, combination in curated_table]:
                    curated_table.append(row)

            for row in curated_table:
                id = str(index_dict[row[0]])
                if row[0] in self.accepting_states:
                    digraph.node(id, id, shape='doublecircle')

                for i, transition in enumerate(row[1][1:]):
                    if transition is not None:
                        digraph.edge(id, str(transition), self.alphabet[i][0])

        compose(self.min_transition_table, self.min_transition_states)

        self.min_graph = digraph

    def dfa_table(self):
        head = ['NFA State', 'DFA State', 'Type'] + [token[0]
                                                     for token in self.alphabet[:-1]]
        body = []

        for i, state in enumerate(self.states):
            type = ''
            if self.nfa.id_final in state:
                type = 'accept'
            elif self.nfa.id_initial in state:
                type = 'initial'

            body.append([', '.join(map(str, state)), get_letter(self.states.index(state)),
                        type] + self.transition_table[i][1:])

        return head, body

    def min_table(self):
        head = ['DFA State', 'min-DFA State', 'Type'] + [token[0]
                                                         for token in self.alphabet[:-1]]
        body = []
        transitions_curated = set(row[1] for row in self.min_transition_table)
        initial_states = [get_letter(self.states.index(
            state)) for state in self.states if self.nfa.id_initial in state]

        for i, state in enumerate(self.min_transition_states):
            actual = None
            type = ''
            for transition in transitions_curated:
                if i == transition[0]:
                    actual = list(transition)[1:]
                    break
            if state[0] in self.accepting_states:
                type = 'accept'
            elif state[0] in initial_states:
                type = 'initial'
            body.append([', '.join(map(str, state)), str(i+1), type] + actual)

        return head, body

    def simulate(self, formatted: list[tuple[str, str]]):
        '''
        Simulate the DFA with a string
        '''
        state_index = 0
        for token in formatted:
            try:
                token_index = self.alphabet.index(token)
            except ValueError:
                return False
            move = self.transition_table[state_index][token_index+1]
            if move is None:
                return False
            else:
                for i in range(len(self.states)):
                    if move == get_letter(i):
                        state_index = i
                        break

        if self.transition_table[state_index][0][1]:
            return True
        return False
