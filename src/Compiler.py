def clean(bf):
    # Removes any non-bf characters from the given program
    return ''.join(char for char in bf if char in "+-<>.,[]")


class Compiler(object):
    def __init__(self, bf):
        self.bf = clean(bf)
        self.compiled = None

    def compile(self):
        self.compiled = []

        #Boilerplate Code for any bf2py program
        self.compiled.append("data = [0] * 30000")
        self.compiled.append("ptr = 0\n")
        self.compiled.append("#bf2py Program Start")

        #indent_count tracks indentation level
        indent_count = 0
        indent = "    "

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
                    if sum_balance > 0:
                        self.compiled.append(indent * indent_count + "data[ptr] += {}".format(sum_balance))
                    else:
                        self.compiled.append(indent * indent_count + "data[ptr] -= {}".format(abs(sum_balance)))
                    sum_balance = 0

            elif char in '<>':
                #This section condenses consecutive <> chars into one line of python
                if char == '>':
                    location_balance += 1
                else:
                    location_balance -= 1
                if next_char not in '<>' and location_balance != 0:
                    #This means that char is the last consecutive < or >
                    if location_balance > 0:
                        self.compiled.append(indent * indent_count + "ptr += {}".format(location_balance))
                    else:
                        self.compiled.append(indent * indent_count + "ptr -= {}".format(abs(location_balance)))
                    location_balance = 0

            elif char == '.':
                self.compiled.append(indent * indent_count + "print(data[ptr])")

            elif char == ',':
                self.compiled.append(indent * indent_count + "data[ptr] = input('Slot {}: '.format(ptr))")

            elif char == '[':
                self.compiled.append(indent * indent_count + "while data[ptr] != 0:")
                indent_count += 1

            elif char == ']':
                indent_count -= 1

        self.compiled = "\n".join(self.compiled)