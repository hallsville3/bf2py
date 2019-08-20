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

        #balance variables track the intermediate value of a sequence of +- chars or <> chars
        sum_balance = 0
        location_balance = 0

        for index in range(len(self.bf)):
            char = self.bf[index]
            next_char = "" if index + 1 == len(self.bf) else self.bf[index + 1]

            if char in '+-':
                #This section condenses consecutive +- chars into one line of python
                if char == '+':
                    sum_balance += 1
                else:
                    sum_balance -= 1
                if next_char not in '+-' and sum_balance != 0:
                    #This means that char is the last consecutive + or -
                    self.compiled += "    " * indents
                    if sum_balance > 0:
                        self.compiled += "data[ptr] += {}\n".format(sum_balance)
                    else:
                        self.compiled += "data[ptr] -= {}\n".format(abs(sum_balance))
                    sum_balance = 0

            elif char in '<>':
                #This section condenses consecutive <> chars into one line of python
                if char == '>':
                    location_balance += 1
                else:
                    location_balance -= 1
                if next_char not in '<>' and location_balance != 0:
                    #This means that char is the last consecutive < or >
                    self.compiled += "    " * indents
                    if location_balance > 0:
                        self.compiled += "ptr += {}\n".format(location_balance)
                    else:
                        self.compiled += "ptr -= {}\n".format(abs(location_balance))
                    location_balance = 0

            elif char == '.':
                self.compiled += "    " * indents
                self.compiled += "print(data[ptr])\n"

            elif char == ',':
                self.compiled += "    " * indents
                self.compiled += "data[ptr] = input('Slot {}: '.format(ptr))\n"

            elif char == '[':
                self.compiled += "    " * indents
                self.compiled += "while data[ptr] != 0:\n"
                indents += 1

            elif char == ']':
                indents -= 1
