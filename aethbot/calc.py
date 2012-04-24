# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

class Math:
    def __init__(self):
        self.stack   = []
        self.symbols = set(['+', '-', '*', '/', '%', '**', '^',
                            '=', 'pop', 'clear', 'list'])

    def push(self, element):
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
        if len(self.stack) > 0:
            removed = self.stack.pop()
            return 'Result: %s' % removed
        else:
            return 'Error: Empty stack'

    def command(self, command):
        elements = command.split()

        # These symbols are handled as 'pop' by the system.
        pop_synonyms = set(['=', 'p'])

        # Handles the elements to be added to the stack.
        for i in range(len(elements)):
            if elements[i] in pop_synonyms:
                elements[i] = 'pop'

            # The common exponent sign is converted to the Python form.
            elif elements[i] == '^':
                elements[i] = '**'

            # Tries to turn them into integers. Otherwise, they are variables.
            if elements[i] not in self.symbols:
                try:
                    elements[i] = int(elements[i])
                except:
                    return 'Error: You can only input numbers or symbols'

        if len(elements) == 0:
            return 'Error: You need to provide at least one element'

        elif len(elements) == 1 and elements[0] == 'pop':
            return self.pop()

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

# For debug purposes, the module can be run directly in a limited interpreter environment.
def main():
    math = Math()
    run  = 'list'

    while (run.upper() != 'Q'):
        print math.command(run)
        run  = raw_input('> ')

if __name__ == '__main__':
    main()
