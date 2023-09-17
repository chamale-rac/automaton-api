import os
from src.expression import Expression
from src._ast import AbstractSyntaxTree
from src._nfa import NonDeterministicFiniteAutomaton
from src._dfa import DeterministicFiniteAutomaton
from src.utils.renderer import Renderer


def read_lines_from_file(file_path):
    with open(file_path, 'r',  encoding='utf-8') as f:
        return f.read().splitlines()


def generate_graphs_for_all_lines(lines):
    renderer = Renderer('./imgs')
    for index, line in enumerate(lines):
        expression = Expression(line)
        expression.shuntingYard()

        abstract_syntax_tree = AbstractSyntaxTree(expression)
        abstract_syntax_tree.build()
        abstract_syntax_tree.rasterize()
        renderer.render(abstract_syntax_tree.graph,
                        'abstract_syntax_tree', index + 1, 'png')

        nfa = NonDeterministicFiniteAutomaton(
            abstract_syntax_tree.builded, expression.alphabet)
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


def select_line_to_generate_graphs(lines):
    line_number = int(input(f"Enter line number (1-{len(lines)}): "))
    if line_number < 1 or line_number > len(lines):
        print("Invalid line number")
        return

    renderer = Renderer('./imgs')

    index = line_number - 1
    expression = Expression(lines[line_number-1])
    expression.shuntingYard()

    abstract_syntax_tree = AbstractSyntaxTree(expression)
    abstract_syntax_tree.build()
    abstract_syntax_tree.rasterize()
    renderer.render(abstract_syntax_tree.graph,
                    'abstract_syntax_tree', index + 1, 'png')

    nfa = NonDeterministicFiniteAutomaton(
        abstract_syntax_tree.builded, expression.alphabet)
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


def select_line_to_simulate(lines):
    line_number = int(input(f"Enter line number (1-{len(lines)}): "))
    if line_number < 1 or line_number > len(lines):
        print("Invalid line number")
        return

    expression = Expression(lines[line_number-1])
    expression.shuntingYard()

    abstract_syntax_tree = AbstractSyntaxTree(expression)
    abstract_syntax_tree.build()

    nfa = NonDeterministicFiniteAutomaton(
        abstract_syntax_tree.builded, expression.alphabet)
    nfa.thompson()

    dfa = DeterministicFiniteAutomaton(nfa, expression.alphabet)
    dfa.subsetsBuild()
    dfa.minimize()

    while True:
        string = input("Enter string to simulate (or 'q' to quit): ")
        if string == 'q':
            break
        test_expression = Expression(string)
        test_expression.format()
        test_expression.format_string()
        print(
            f'{string} on {lines[line_number-1]} using NFA => {nfa.simulate(test_expression.formatted)}')
        print(
            f'{string} on {lines[line_number-1]} using DFA => {dfa.simulate(test_expression.formatted)}')
        print(
            f'{string} on {lines[line_number-1]} using min-DFA => {dfa.simulate(test_expression.formatted)}')


def main():
    file_path = input("Enter file path (./default.txt): ")
    if not os.path.isfile(file_path):
        print("Invalid file path")
        return
    lines = read_lines_from_file(file_path)
    while True:
        print("1. Generate graphs for all lines")
        print("2. Select line to generate graphs for")
        print("3. Select line to simulate with many strings")
        print("4. Quit")
        choice = input("Enter choice (1-4): ")
        if choice == '1':
            generate_graphs_for_all_lines(lines)
        elif choice == '2':
            select_line_to_generate_graphs(lines)
        elif choice == '3':
            select_line_to_simulate(lines)
        elif choice == '4':
            break
        else:
            print("Invalid choice")


if __name__ == '__main__':
    main()
