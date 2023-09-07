from src.expression import Expression
from src._ast import AbstractSyntaxTree
from src.utils.tools import to_base64
import time


def AbstractSyntaxTreeWrapper(regex: str, HEIGHT_REGEX, WIDTH_REGEX):
    start_time = time.time()
    expression = Expression(regex)
    expression.shuntingYard()
    ast = AbstractSyntaxTree(expression)
    ast.build()
    ast.rasterize(web=True)
    end_time = time.time()
    string, width, height = to_base64(ast.graph.pipe(
        format='svg'), HEIGHT_REGEX, WIDTH_REGEX)

    return {
        'src': 'data:image/svg+xml;base64,' + string,
        'alt': 'Abstract Syntax Tree',
        'width': width,
        'height': height,
        'title': 'Abstract Syntax Tree',
        'description': f'\nYour expression: {regex}'
    }
