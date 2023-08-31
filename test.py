from src.expression import Expression


def testExpression():
    '''
    Test notes:
        1. For input a special character just \ before it
        2. [] for a group of characters, - for a range of characters just works once. Example: [a-z] or [0-9] works, [a-z0-9] not works, use [a-z]|[0-9] instead

    '''
    especial_test = input('Special expression: ') or 'ab\\nc'

    expressions = ['(a|t)c', '(a|b)*', '(a*|b*)*', '((ε|a)|b*)*', '(a|b)*abb(a|b)*', '0?(1?)?0*',
                   'if\\([ae]+\\)\\{[ei]+\\}(\\n(else\\{[jl]+\\}))?', '[ae03]+@[ae03]+.(com|net|org)(.(gt|cr|co))?', '[ae03]', '[a-e]', '[0-3]', '[a-e]|[0-3]']

    results = ['at|c•', 'ab|*', 'a*b*|*', 'εa|b*|*', 'ab|*a•b•b•ab|*•', '0?1??•0*•',
               'if•(•ae|+•)•{•ei|+•}•nel•s•e•{•jl|+•}••?•', 'ae|0|3|+@•ae|0|3|+•.•co•m•ne•t•|or•g•|•.gt•cr•|co•|•?•', 'ae|0|3|', 'ab|c|d|e|', '01|2|3|', 'ab|c|d|e|01|2|3||']

    for index in range(len(expressions)):
        expression = Expression(expressions[index])
        expression.shuntingYard()
        print(
            f' >> INFIX := {expressions[index]} => POSTFIX := {expression.postfixString()}')
        assert expression.postfixString() == results[index]

    expression = Expression(especial_test)
    expression.shuntingYard()
    print(
        f' >> INFIX := {especial_test} => POSTFIX := {expression.postfixString()}')


testExpression()
