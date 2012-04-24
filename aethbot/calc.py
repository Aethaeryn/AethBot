# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

import math, string
import irclib

class Math:
    def __init__(self, mode):
        self.mode   = mode
        self.switch_mode(self.mode)

    def switch_mode(self, mode):
        self.mode = mode
        if mode == "postfix":
            self.math = PostfixMath()

    def command(self, command):
        return self.math.command(command)

class PostfixMath:
    def __init__(self):
        self.stack   = []
        self.symbols = set(["+", "-", "*", "/", "%", "**", "^",
                            "=", "pop", "clear", "list"])

    def push(self, element):
        if element not in self.symbols:
            self.stack.append(element)
            return "Item pushed onto stack"

        elif element == "pop":
            return self.pop()

        elif element == "clear":
            self.stack = []
            return "The stack has been cleared"

        elif element == "list":
            stack = "Items on stack: "

            for item in self.stack:
                stack += str(item)
                stack += " "

            if len(self.stack) == 0:
                stack += "None "

            return stack[:-1]

        elif element in self.symbols:
            if len(self.stack) >= 2:
                a = self.stack.pop()
                b = self.stack.pop()

                operation = str(b) + element + str(a)

                if element == "**" and (len(str(a)) > 2 or len(str(b)) > 2):
                    return "Error: Both numbers can only be two digits or less in an exponential operation"

                try:
                    result = eval(operation)
                    return self.push(result)
                except ArithmeticError as detail:
                    return "Error: " + str(detail)

            else:
                return "Error: Attempted operation requires at least two elements on stack"

    def pop(self):
        if len(self.stack) > 0:
            removed = self.stack.pop()
            return "Result: %s" % removed
        else:
            return "Error: Empty stack"

    def command(self, command):
        elements = command.split()

        # These symbols are handled as 'pop' by the system.
        pop_synonyms = set(["=", "p"])

        # Handles the elements to be added to the stack.
        for i in range(len(elements)):
            if elements[i] in pop_synonyms:
                elements[i] = "pop"

            # The common exponent sign is converted to the Python form.
            elif elements[i] == "^":
                elements[i] = "**"

            # Tries to turn them into integers. Otherwise, they are variables.
            if elements[i] not in self.symbols:
                try:
                    elements[i] = int(elements[i])
                except:
                    return "Error: You can only input numbers or symbols"

        if len(elements) == 0:
            return "Error: You need to provide at least one element"

        elif len(elements) == 1 and elements[0] == "pop":
            return self.pop()

        elif len(elements) == 1:
            return self.push(elements[0])

        else:
            outputs = []

            for element in elements:
                outputs.append(self.push(element))

            outputStrings = ""

            for output in outputs:
                if string.find(output, "cleared") != -1 or string.find(output, "Result:") != -1 or string.find(output, "Error:") != -1 or string.find(output, "Items on stack") != -1:
                    outputStrings += output
                    outputStrings += "; "

            if len(outputStrings) > 0:
                return outputStrings

            return "Items pushed onto stack"

# For debug purposes, the module can be run directly in a limited interpreter environment.
def main():
    math = Math("postfix")
    run  = "list"

    while (run.upper() != "Q"):
        print math.command(run)
        run  = raw_input("> ")

if __name__ == '__main__':
    main()
