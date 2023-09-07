from src.expression import Expression
from src._ast import AbstractSyntaxTree
from src._nfa import NonDeterministicFiniteAutomaton
from src.utils.tools import to_base64


def wrapper(regex: str, HEIGHT_REGEX, WIDTH_REGEX):
    expression = Expression(regex)
    expression.shuntingYard()
    ast = AbstractSyntaxTree(expression)
    ast.build()
    ast.rasterize(web=True)
    string, width, height = to_base64(ast.graph.pipe(
        format='svg'), HEIGHT_REGEX, WIDTH_REGEX)

    AST = {
        'src': 'data:image/svg+xml;base64,' + string,
        'alt': 'Abstract Syntax Tree',
        'width': width,
        'height': height,
        'title': 'Abstract Syntax Tree',
        'description': f'\nYour expression: {regex}'
    }

    nfa = NonDeterministicFiniteAutomaton(ast.builded)
    nfa.thompson()
    nfa.rasterize(web=True)
    string, width, height = to_base64(nfa.graph.pipe(
        format='svg'), HEIGHT_REGEX, WIDTH_REGEX)

    NFA = {
        'src': 'data:image/svg+xml;base64,' + string,
        'alt': 'Non Deterministic Finite Automaton',
        'width': width,
        'height': height,
        'title': 'Non Deterministic Finite Automaton',
        'description': f'\nYour expression: {regex}'
    }

    return [AST, NFA]
