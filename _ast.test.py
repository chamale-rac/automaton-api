import time
from src.expression import Expression
from src._ast import AbstractSyntaxTree
from src.utils.renderer import Renderer


start_time = time.time()

lines = ['(a|t)c', '(a|b)*', '(a*|b*)*', '((ε|a)|b*)*', '(a|b)*abb(a|b)*', '0?(1?)?0*',
         'if\\([ae]+\\)\\{[ei]+\\}(\\n(else\\{[jl]+\\}))?', '[ae03]+@[ae03]+.(com|net|org)(.(gt|cr|co))?', '[ae03]', '[a-e]', '[0-3]', '[a-e]|[0-3]']


renderer = Renderer('./imgs')
for index, line in enumerate(lines):
    expression = Expression(line)
    expression.shuntingYard()
    abstract_syntax_tree = AbstractSyntaxTree(expression)
    abstract_syntax_tree.build()
    abstract_syntax_tree.rasterize()
    renderer.render(abstract_syntax_tree.graph,
                    'abstract_syntax_tree', index + 1, 'svg')


end_time = time.time()
print(f"Execution took {end_time - start_time:.2f} seconds to run.")
