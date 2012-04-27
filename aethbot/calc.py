# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://opensource.org/licenses/MIT

'''This is a postfix (RPN) calculator module for AethBot.
'''

class Math:
    '''Sets up a basic postfix (RPN) calculator that uses stacks to do
    computations that are then returned to the bot.
    '''
    def __init__(self):
        '''Sets up the calculator.
        '''
        self.stack   = []
        self.symbols = set(['+', '-', '*', '/', '%', '**',
                            'pop', 'clear', 'list', 'sum'])

    def push(self, element):
        '''Pushes an item onto the top of the stack unless the element
        being pushed is a special command. In that case, some sort of
        action is taken, depending on the command.
        '''
        if element not in self.symbols:
            self.stack.append(element)
            return 'Item pushed onto stack'

        elif element == 'pop':
            return self.pop()

        elif element == 'clear':
            self.stack = []
            return 'The stack has been cleared'

        elif element == 'list':
            stack = 'Items on stack: '

            for item in self.stack:
                stack += str(item)
                stack += ' '

            if len(self.stack) == 0:
                stack += 'None '

            return stack[:-1]

        elif element == 'sum':
            return self.push(sum(self.stack))

        elif element in self.symbols:
            if len(self.stack) >= 2:
                first  = self.stack.pop()
                second = self.stack.pop()

                operation = str(second) + element + str(first)

                if element == '**' and (len(str(first)) > 2 or len(str(second)) > 2):
                    return 'Error: Both numbers can only be two digits or less in an exponential operation'

                try:
                    result = eval(operation)
                    return self.push(result)
                except ArithmeticError as detail:
                    return 'Error: ' + str(detail)

            else:
                return 'Error: Attempted operation requires at least two elements on stack'

    def pop(self):
        '''Pops the top item from the stack and reveals what it is.
        '''
        if len(self.stack) > 0:
            removed = self.stack.pop()
            return 'Result: %s' % removed
        else:
            return 'Error: Empty stack'

    def substitute(self, element):
        '''If a substitute can be made, it is made.
        '''
        pop_synonyms = set(['=', 'p'])

        if element in pop_synonyms:
            return 'pop'

        elif element == '^':
            return '**'

        return element

    def command(self, command):
        '''Takes in a calculator command and returns a result to be
        printed by the bot. They must be a recognized symbol, an
        equivalent to that symbol, or a number.
        '''
        elements = command.split()

        for i in range(len(elements)):
            if elements[i] not in self.symbols:
                try:
                    elements[i] = int(elements[i])
                except:
                    return 'Error: You can only input numbers or symbols'

            else:
                elements[i] = self.substitute(elements[i])

        if len(elements) == 0:
            return 'Error: You need to provide at least one element'

        elif len(elements) == 1:
            return self.push(elements[0])

        else:
            outputs = []

            for element in elements:
                outputs.append(self.push(element))

            output_strings = ''

            for output in outputs:
                if output.find('cleared') != -1 or output.find('Result:') != -1 or output.find('Error:') != -1 or output.find('Items on stack') != -1:
                    output_strings += output
                    output_strings += '; '

            if len(output_strings) > 0:
                return output_strings

            return 'Items pushed onto stack'

def main():
    '''Creates a limited interpreter environment so that this module
    can be run and tested directly instead of requiring the entire bot
    to be run.
    '''
    math = Math()
    run  = 'list'

    while (run.upper() != 'Q'):
        print math.command(run)
        run  = raw_input('> ')

if __name__ == '__main__':
    main()
