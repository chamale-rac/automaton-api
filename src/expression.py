#!/usr/bin/env python

"""expression.py: Shunting yard algorithm implementation for regular expressions"""

__author__ = "Samuel A. Chamalé"
__email__ = "cha21881@uvg.edu.gt"

__copyright__ = "Copyright 2023, neo-automaton-basic-toolkit"
__license__ = "GPL"
__version__ = "1.0.1"

__status__ = "Production"


class Expression:
    def __init__(self, expression):
        self.infix = expression

        self.postfix = None
        self.postfix_string = None
        self.formatted = None
        self.alphabet = None

        self.all_operators = ['|', '?', '+', '*', '^']
        self.binary_operators = ['|', '^']
        self.precedence = {'(': 1, '|': 2, '•': 3, '?': 4,
                           '*': 4, '+': 4, '^': 5}

    def getPostfixString(self):
        '''
        Convert the postfix expression to a string

        :return: string
        '''
        return ''.join([token[0] for token in self.postfix])

    def shuntingYard(self):
        '''
        Implementation of the shunting yard algorithm.

        :notes: 
            - types: grouping, operator, escaped, character

        :return: a list of tokens in postfix notation
        '''
        postfix = []
        stack = []
        self.format()

        for index in range(len(self.formatted)):
            token = self.formatted[index]

            if token == ('(', 'grouping'):
                stack.append(token)
            elif token == (')', 'grouping'):
                while stack and stack[-1] != ('(', 'grouping'):
                    postfix.append(stack.pop())
                if stack:
                    stack.pop()
            else:
                while stack:
                    peeked_token = stack[-1]
                    if peeked_token[1] == 'grouping' or peeked_token[1] == 'operator':
                        peeked_token_precedence = self.precedence.get(
                            peeked_token[0], 6)
                    else:
                        peeked_token_precedence = 6

                    if token[1] == 'grouping' or token[1] == 'operator':
                        token_precedence = self.precedence.get(token[0], 6)
                    else:
                        token_precedence = 6
                    if peeked_token_precedence >= token_precedence:
                        postfix.append(stack.pop())
                    else:
                        break
                stack.append(token)

        while stack:
            postfix.append(stack.pop())

        self.postfix = postfix
        self.postfix_string = self.getPostfixString()

    def format(self):
        '''
        Add implicit concatenation operators to the infix expression

        :return: set of tuples containing the type and char of each token
        '''
        infix_length = len(self.infix)
        result = []

        def checkConcatenation(index, offset):
            '''
            Check if an implicit concatenation operator is needed

            :return: boolean
            '''
            if index+offset < infix_length and self.infix[index] != '(' and self.infix[index+offset] != ')' and self.infix[index] not in self.binary_operators and self.infix[index+offset] not in self.all_operators:
                result.append(('•', 'operator'))

        index = 0
        while index < infix_length:
            match self.infix[index]:
                case '\\':
                    result.append((self.infix[index + 1], 'escaped'))
                    checkConcatenation(index, 2)
                    index += 2
                case '[':
                    close_index = self.infix.find(']', index)
                    inner_group = self.infix[index:close_index]
                    if '-' in inner_group:
                        result.append(('(', 'grouping'))
                        for local_index in range(index+1, close_index):
                            if self.infix[local_index] == '-':
                                continue
                            elif local_index+2 < close_index and self.infix[local_index+1] == '-' and self.infix[local_index+2].isalnum():
                                for inner_index in range(ord(self.infix[local_index]), ord(self.infix[local_index+2])+1):
                                    result.append(
                                        (chr(inner_index), 'character'))
                                    if inner_index != ord(self.infix[local_index+2]):
                                        result.append(('|', 'operator'))
                                index = local_index+2
                                break
                            else:
                                result.append(
                                    (self.infix[local_index], 'character'))
                                if local_index+1 < close_index and self.infix[local_index+1] != ']':
                                    result.append(('|', 'operator'))
                    else:
                        result.append(('(', 'grouping'))
                        for local_index in range(index+1, close_index):
                            result.append(
                                (self.infix[local_index], 'character'))
                            if local_index+1 < close_index and self.infix[local_index+1] != ']':
                                result.append(('|', 'operator'))
                    result.append((')', 'grouping'))
                    index = close_index+1
                case _:
                    if self.infix[index] in self.all_operators:
                        result.append((self.infix[index], 'operator'))
                    elif self.infix[index] == '(' or self.infix[index] == ')':
                        result.append((self.infix[index], 'grouping'))
                    else:
                        result.append((self.infix[index], 'character'))
                    checkConcatenation(index, 1)
                    index += 1

        self.formatted = result
        self.alphabet = set(
            filter(lambda x: x[1] in ['escaped', 'character'], result))
