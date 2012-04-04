#    AethBot Math Module
#    Copyright (C) 2011, 2012 Michael Babich
#
#    This program is free software. It comes without any warranty, to
#    the extent permitted by applicable law. You can redistribute it
#    and/or modify it under the terms of the Do What The Fuck You Want
#    To Public License, Version 2, as published by Sam Hocevar. See
#    http://sam.zoy.org/wtfpl/COPYING for more details.


# Default Python modules.
import math, string

# python-irclib modules.
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
        
        # Handles the elements to be added to the stack.
        for i in range(len(elements)):
            # The equals is equivalent to pop.
            if elements[i] == "=":
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

    while (string.upper(run) != "Q"):
        print math.command(run)
        run  = raw_input("> ")

if __name__ == '__main__':
    main()
