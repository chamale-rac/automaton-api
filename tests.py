def testExpression():
    '''
    Test notes:
        1. For input a special character just \ before it
        2. [] for a group of characters, - for a range of characters just works once. Example: [a-z] or [0-9] works, [a-z0-9] not works, use [a-z]|[0-9] instead

    '''
    from src.expression import Expression
    from src._ast import AbstractSyntaxTree
    from src.utils.renderer import Renderer
    # especial_test = input('Special expression: ') or 'ab\\nc'

    expressions = ['(a|t)c', '(a|b)*', '(a*|b*)*', '((ϵ|a)|b*)*', '(a|b)*abb(a|b)*', '0?(1?)?0*',
                   'if\\([ae]+\\)\\{[ei]+\\}(\\n(else\\{[jl]+\\}))?', '[ae03]+@[ae03]+.(com|net|org)(.(gt|cr|co))?', '[ae03]', '[a-e]', '[0-3]', '[a-e]|[0-3]']

    results = ['at|c•', 'ab|*', 'a*b*|*', 'ϵa|b*|*', 'ab|*a•b•b•ab|*•', '0?1??•0*•',
               'if•(•ae|+•)•{•ei|+•}•nel•s•e•{•jl|+•}••?•', 'ae|0|3|+@•ae|0|3|+•.•co•m•ne•t•|or•g•|•.gt•cr•|co•|•?•', 'ae|0|3|', 'ab|c|d|e|', '01|2|3|', 'ab|c|d|e|01|2|3||']

    for index in range(len(expressions)):
        expression = Expression(expressions[index])
        expression.shuntingYard()
        # print('TOKENS:', expression.tokens)
        # print(
        #     f' >> INFIX := {expressions[index]} => POSTFIX := {expression.postfix_string}')
        abstract_syntax_tree = AbstractSyntaxTree(expression)
        abstract_syntax_tree.build()
        abstract_syntax_tree.rasterize()
        renderer = Renderer('./imgs', index + 1)
        renderer.render(abstract_syntax_tree.graph,
                        'abstract_syntax_tree', 'png')
        assert expression.postfix_string == results[index]

    # expression = Expression(especial_test)
    # expression.shuntingYard()
    # print(
    #     f' >> INFIX := {especial_test} => POSTFIX := {expression.postfixString()}')


def testAST():
    import time
    from src.expression import Expression
    from src._ast import AbstractSyntaxTree
    from src.utils.renderer import Renderer

    start_time = time.time()

    lines = ['(a|t)c', '(a|b)*', '(a*|b*)*', '((ϵ|a)|b*)*', '(a|b)*abb(a|b)*', '0?(1?)?0*',
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


def testNFA():
    import time
    from src.expression import Expression
    from src._ast import AbstractSyntaxTree
    from src._nfa import NonDeterministicFiniteAutomaton
    from src.utils.renderer import Renderer

    start_time = time.time()

    lines = ['(a|t)c', '(a|b)*', '(a*|b*)*', '((ϵ|a)|b*)*', '(a|b)*abb(a|b)*', '0?(1?)?0*',
             'if\\([ae]+\\)\\{[ei]+\\}(\\n(else\\{[jl]+\\}))?', '[ae03]+@[ae03]+.(com|net|org)(.(gt|cr|co))?', '[ae03]', '[a-e]', '[0-3]', '[a-e]|[0-3]']

    renderer = Renderer('./imgs')
    for index, line in enumerate(lines):
        expression = Expression(line)
        expression.shuntingYard()
        abstract_syntax_tree = AbstractSyntaxTree(expression)
        abstract_syntax_tree.build()
        abstract_syntax_tree.rasterize()
        renderer.render(abstract_syntax_tree.graph,
                        'abstract_syntax_tree', index + 1, 'png')
        nfa = NonDeterministicFiniteAutomaton(abstract_syntax_tree.builded)
        nfa.thompson()
        nfa.rasterize()
        renderer.render(nfa.graph, 'nfa', index + 1, 'png')

    end_time = time.time()
    print(f"Execution took {end_time - start_time:.2f} seconds to run.")


def testDFA():
    import time
    from src.expression import Expression
    from src._ast import AbstractSyntaxTree
    from src._nfa import NonDeterministicFiniteAutomaton
    from src.utils.renderer import Renderer
    from src._dfa import DeterministicFiniteAutomaton

    start_time = time.time()

    lines = ['(a|t)c', '(a|b)*', '(a*|b*)*', '((ϵ|a)|b*)*', '(a|b)*abb(a|b)*', '0?(1?)?0*',
             'if\\([ae]+\\)\\{[ei]+\\}(\\n(else\\{[jl]+\\}))?', '[ae03]+@[ae03]+.(com|net|org)(.(gt|cr|co))?', '[ae03]', '[a-e]', '[0-3]', '[a-e]|[0-3]']

    lines = ['0?(1?)?0*']

    renderer = Renderer('./imgs')
    for index, line in enumerate(lines):
        expression = Expression(line)
        expression.shuntingYard()
        abstract_syntax_tree = AbstractSyntaxTree(expression)
        abstract_syntax_tree.build()
        abstract_syntax_tree.rasterize()
        renderer.render(abstract_syntax_tree.graph,
                        'abstract_syntax_tree', index + 1, 'png')
        nfa = NonDeterministicFiniteAutomaton(abstract_syntax_tree.builded)
        nfa.thompson()
        nfa.rasterize()
        renderer.render(nfa.graph, 'nfa', index + 1, 'png')

        dfa = DeterministicFiniteAutomaton(nfa, expression.alphabet)
        dfa.subsetsBuild()
        dfa.rasterize()
        renderer.render(dfa.graph, 'dfa', index+1, 'png')

        dfa.minimize()
        head, body = dfa.dfa_table()
        print(head)
        for row in body:
            print(row)

        head, body = dfa.min_table()
        print(head)
        for row in body:
            print(row)

    end_time = time.time()
    print(f"Execution took {end_time - start_time:.2f} seconds to run.")


def testMIN_DFA():
    import time
    from src.expression import Expression
    from src._ast import AbstractSyntaxTree
    from src._nfa import NonDeterministicFiniteAutomaton
    from src.utils.renderer import Renderer
    from src._dfa import DeterministicFiniteAutomaton

    lines = ['(a|t)c', '(a|b)*', '(a*|b*)*', '((ϵ|a)|b*)*', '(a|b)*abb(a|b)*', '0?(1?)?0*',
             'if\\([ae]+\\)\\{[ei]+\\}(\\n(else\\{[jl]+\\}))?', '[ae03]+@[ae03]+.(com|net|org)(.(gt|cr|co))?', '[ae03]', '[a-e]', '[0-3]', '[a-e]|[0-3]']

    lines = ['(a|e|0|3)+@(a|e|0|3)+.(com|net|org)(.(gt|cr|co))?']

    renderer = Renderer('./imgs')
    for index, line in enumerate(lines):

        start_time = time.time()
        expression = Expression(line)
        expression.shuntingYard()
        abstract_syntax_tree = AbstractSyntaxTree(expression)
        abstract_syntax_tree.build()
        abstract_syntax_tree.rasterize()
        renderer.render(abstract_syntax_tree.graph,
                        'abstract_syntax_tree', index + 1, 'png')
        nfa = NonDeterministicFiniteAutomaton(abstract_syntax_tree.builded)
        nfa.thompson()
        nfa.rasterize()
        renderer.render(nfa.graph, 'nfa', index + 1, 'png')

        dfa = DeterministicFiniteAutomaton(nfa, expression.alphabet)
        dfa.subsetsBuild()
        dfa.rasterize()
        renderer.render(dfa.graph, 'dfa', index+1, 'png')

        dfa.minimize()
        dfa.min_rasterize()

        renderer.render(dfa.min_graph, 'min_dfa', index+1, 'png')

        end_time = time.time()
        print(f"Execution took {end_time - start_time:.2f} seconds to run.")


def testSimulate_NFA():
    import time
    from src.expression import Expression
    from src._ast import AbstractSyntaxTree
    from src._nfa import NonDeterministicFiniteAutomaton
    from src._dfa import DeterministicFiniteAutomaton

    lines = ['(a|b)*c']

    for index, line in enumerate(lines):
        start_time = time.time()

        expression = Expression(line)
        expression.shuntingYard()

        abstract_syntax_tree = AbstractSyntaxTree(expression)
        abstract_syntax_tree.build()

        nfa = NonDeterministicFiniteAutomaton(
            abstract_syntax_tree.builded, expression.alphabet)
        nfa.thompson()

        dfa = DeterministicFiniteAutomaton(nfa, expression.alphabet)
        dfa.subsetsBuild()

        for string in ['ab', 'ac', 'aaabac', 'babc']:
            expression = Expression(string)
            expression.format()
            expression.format_string()
            print(f'{string} => ------------------------------------')
            print(f'{string} => {nfa.simulate(expression.formatted)}')
            print(f'{string} => {dfa.simulate(expression.formatted)}')

            EXPRESSION = ''
            for token in expression.formatted:
                EXPRESSION += token[0]

        end_time = time.time()
        print(f"Execution took {end_time - start_time:.2f} seconds to run.")


testSimulate_NFA()
