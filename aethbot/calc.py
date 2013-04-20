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
        self.symbols = set(['+', '-', '*', '/', '%', 'exp',
                            'clear', 'list', 'sum', '='])

    def push(self, element):
        '''Pushes an item onto the top of the stack unless the element
        being pushed is a special command. In that case, some sort of
        action is taken, depending on the command.
        '''
        if element not in self.symbols:
            self.stack.append(element)
            return

        elif element == '=':
            return self.pop()

        elif element == 'clear':
            self.stack = []
            return

        elif element == 'list':
            return str(self.stack).translate(None, ',')

        elif element == 'sum':
            stack_sum = sum(self.stack)
            self.push('clear')
            return self.push(stack_sum)

        elif element in self.symbols:
            if len(self.stack) >= 2:
                first  = self.stack.pop()
                second = self.stack.pop()

                if element == 'exp':
                    if (len(str(first)) > 2 or len(str(second)) > 2):
                        return 'Error: Both numbers can only be two digits or less in an exponential operation'
                    else:
                        element = "**"

                operation = str(second) + element + str(first)

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
            return str(self.stack.pop())
        else:
            return 'Error: Empty stack'

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

        if len(elements) == 0:
            return 'Error: You need to provide at least one element'

        else:
            outputs = []

            for element in elements:
                outputs.append(self.push(element))

            output_strings = ''

            for output in outputs:
                if output:
                    output_strings += output
                    output_strings += '; '

            if len(output_strings) > 0:
                return output_strings

            return

def main():
    '''Creates a limited interpreter environment so that this module
    can be run and tested directly instead of requiring the entire bot
    to be run.
    '''
    math = Math()
    run  = 'list'

    while (run.upper() != 'Q'):
        result = math.command(run)

        if result:
            print result

        run  = raw_input('> ')

if __name__ == '__main__':
    main()
