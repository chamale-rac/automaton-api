class Expression:
    def __init__(self, expression):
        self.infix = expression

        self.postfix = []
        self.tokens = set()

        self.all_operators = ['|', '?', '+', '*', '^']
        self.binary_operators = ['|', '^']

    def shuntingYard(self):
        '''
        Implementation of the shunting yard algorithm

        :return: a list of tokens in postfix notation
        '''
        stack = []
        self.format()

        pass

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
                result.append(tuple('•', 'concat'))

        def nothingMatched(index):
            '''
            Handle the rest of cases where no initial cases matched
            '''
            if self.infix[index] in self.all_operators:
                result.append(tuple(self.infix[index], 'operator'))
            elif self.infix[index] == '(' or self.infix[index] == ')':
                result.append(tuple(self.infix[index], 'grouping'))
            else:
                result.append(tuple(self.infix[index], 'character'))
            checkConcatenation(index, 1)

        index = 0
        while index < infix_length:
            match self.infix[index]:
                case '\\':
                    result.append(tuple(self.infix[index + 1], 'escaped'))
                    checkConcatenation(index, 2)
                    index += 2
                case '[':
                    close_index = self.infix.find(']', index)
                    inner_group = self.infix[index:close_index]
                    if '-' in inner_group:
                        result.append(tuple('(', 'grouping'))
                        for local_index in range(index+1, close_index):
                            if self.infix[local_index] == '-':
                                continue
                            elif local_index+2 < close_index and self.infix[local_index+1] == '-' and self.infix[local_index+2].isalnum():
                                for inner_index in range(ord(self.infix[local_index]), ord(self.infix[local_index+2])+1):
                                    result.append(
                                        tuple(chr(inner_index), 'character'))
                                    if inner_index != ord(self.infix[local_index+2]):
                                        result.append(tuple('|', 'or'))
                                index = local_index+2
                                break
                            else:
                                result.append(
                                    tuple(self.infix[local_index], 'character'))
                                if local_index+1 < close_index and self.infix[local_index+1] != ']':
                                    result.append(tuple('|', 'or'))
                    else:
                        result.append(tuple('(', 'grouping'))
                        for local_index in range(index+1, close_index):
                            result.append(
                                tuple(self.infix[local_index], 'character'))
                            if local_index+1 < close_index and self.infix[local_index+1] != ']':
                                result.append(tuple('|', 'or'))
                    result.append(tuple(')', 'grouping'))
                    index = close_index+1
                case _:
                    nothingMatched(index)
                    i += 1

        self.postfix = result
        self.tokens = set(
            filter(lambda x: x[1] in ['escaped', 'character'], result))
