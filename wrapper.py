from src.expression import Expression
from src._ast import AbstractSyntaxTree
from src._nfa import NonDeterministicFiniteAutomaton
from src._dfa import DeterministicFiniteAutomaton
from src.utils.tools import to_base64


def wrapper_graphs(regex: str, HEIGHT_REGEX, WIDTH_REGEX):
    expression = Expression(regex)
    expression.shuntingYard()
    ast = AbstractSyntaxTree(expression)
    ast.build()
    ast.rasterize(web=True)
    string, width, height = to_base64(ast.graph.pipe(
        format='svg'), HEIGHT_REGEX, WIDTH_REGEX)

    AST = {
        'src': 'data:image/svg+xml;base64,' + string,
        'alt': 'Abstract Syntax Tree ',
        'width': width,
        'height': height,
        'title': 'ATS (Abstract Syntax Tree)',
        'description': f'\nUsing: {regex}'
    }

    nfa = NonDeterministicFiniteAutomaton(ast.builded, expression.alphabet)
    nfa.thompson()
    nfa.rasterize(web=True)
    string, width, height = to_base64(nfa.graph.pipe(
        format='svg'), HEIGHT_REGEX, WIDTH_REGEX)

    NFA = {
        'src': 'data:image/svg+xml;base64,' + string,
        'alt': 'Non Deterministic Finite Automaton',
        'width': width,
        'height': height,
        'title': 'NFA (Non Deterministic Finite Automaton)',
        'description': f'\nUsing: {regex}'
    }

    dfa = DeterministicFiniteAutomaton(nfa, expression.alphabet)
    dfa.subsetsBuild()
    dfa.rasterize(web=True)

    string, width, height = to_base64(dfa.graph.pipe(
        format='svg'), HEIGHT_REGEX, WIDTH_REGEX)

    DFA = {
        'src': 'data:image/svg+xml;base64,' + string,
        'alt': 'Deterministic Finite Automaton',
        'width': width,
        'height': height,
        'title': 'DFA (Deterministic Finite Automaton)',
        'description': f'\nUsing: {regex}'
    }

    dfa.minimize()
    dfa.min_rasterize(web=True)

    string, width, height = to_base64(
        dfa.min_graph.pipe(format='svg'), HEIGHT_REGEX, WIDTH_REGEX)

    MIN_DFA = {
        'src': 'data:image/svg+xml;base64,' + string,
        'alt': 'Minimized Deterministic Finite Automaton',
        'width': width,
        'height': height,
        'title': 'min-DFA (Minimized Deterministic Finite Automaton)',
        'description': f'\nUsing: {regex}'
    }

    head, body = dfa.dfa_table()

    DFA_TABLE = {
        'title': 'NFA to DFA state table',
        'head': head,
        'body': body,
    }

    head, body = dfa.min_table()

    MIN_TABLE = {
        'title': 'DFA to min-DFA state table',
        'head': head,
        'body': body,
    }

    return [AST, NFA, DFA, MIN_DFA], [DFA_TABLE, MIN_TABLE]


def wrapper_simulation(regex: str, strings: list[str]):
    head = ['Input', 'Used as', 'NFA', 'DFA', 'min-DFA']
    body = []

    expression = Expression(regex)
    expression.shuntingYard()

    ast = AbstractSyntaxTree(expression)
    ast.build()

    nfa = NonDeterministicFiniteAutomaton(ast.builded, expression.alphabet)
    nfa.thompson()

    dfa = DeterministicFiniteAutomaton(nfa, expression.alphabet)
    dfa.subsetsBuild()
    dfa.minimize()

    for i, string in enumerate(strings):
        expression = Expression(string)
        expression.format()
        expression.format_string()

        in_nfa = nfa.simulate(expression.formatted)
        in_dfa = dfa.simulate(expression.formatted)
        in_min_dfa = dfa.min_simulate(expression.formatted)

        used = ''
        for token in expression.formatted:
            used += token[0]

        body.append([string, used, str(in_nfa), str(in_dfa), str(in_min_dfa)])

    RES_TABLE = {
        'title': 'Simulation results',
        'head': head,
        'body': body,
    }

    return [RES_TABLE]
