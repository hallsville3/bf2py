def clean(bf):
    # Removes any non-bf characters from the given program
    return ''.join(char for char in bf if char in "+-<>.,[]")


class Compiler(object):
    def __init__(self, bf):
        self.bf = clean(bf)
        self.compiled = None

    def compile(self):
        #Boilerplate Code for any bf2py program
        self.compiled = "data = [0] * 30000\n"
        self.compiled += "ptr = 0\n\n#bf2py Program Start\n"

        #indents tracks indentation level
        indents = 0

        #balance tracks the intermediate value of a sequence of +- chars
        balance = 0

        for index in range(len(self.bf)):
            char = self.bf[index]
            next_char = "" if index + 1 == len(self.bf) else self.bf[index + 1]

            if char in '+-':
                #This section condenses consecutive +- chars into one line of python
                if char == '+':
                    balance += 1
                else:
                    balance -= 1
                if next_char not in '+-' and balance != 0:
                    #This means that char is the last consecutive + or -
                    self.compiled += "\t" * indents
                    if balance > 0:
                        self.compiled += "data[ptr] += {}\n".format(balance)
                    else:
                        self.compiled += "data[ptr] -= {}\n".format(abs(balance))
                    balance = 0

            elif char == '<':
                self.compiled += "\t" * indents
                self.compiled += "ptr -= 1\n"

            elif char == '>':
                self.compiled += "\t" * indents
                self.compiled += "ptr += 1\n"

            elif char == '.':
                self.compiled += "\t" * indents
                self.compiled += "print(data[ptr])\n"

            elif char == ',':
                self.compiled += "\t" * indents
                self.compiled += "data[ptr] = input('Slot {}: '.format(ptr))\n"

            elif char == '[':
                self.compiled += "\t" * indents
                self.compiled += "while data[ptr] != 0:\n"
                indents += 1

            elif char == ']':
                indents -= 1
