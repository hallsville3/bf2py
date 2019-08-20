def clean(bf):
    # Removes any non-bf characters from the given program and returns as a list
    return [char0 for char0 in bf if char0 in "+-<>.,[]"]


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

        index = 0
        while index < len(self.bf):
            char0 = self.bf[index]
            char1 = "\0" if index + 1 == len(self.bf) else self.bf[index + 1]
            char2 = "\0" if index + 2 >= len(self.bf) else self.bf[index + 2]
            print "hi"
            if char0 + char1 + char2 == "[-]":
                self.compiled.append(indent * indent_count + "data[ptr] = 0")
                index += 2
            elif char0 in '+-':
                #This section condenses consecutive +- chars into one line of python
                if char0 == '+':
                    sum_balance += 1
                else:
                    sum_balance -= 1
                if char1 not in '+-' and sum_balance != 0:
                    #This means that char0 is the last consecutive + or -
                    if sum_balance > 0:
                        self.compiled.append(indent * indent_count + "data[ptr] += {}".format(sum_balance))
                    else:
                        self.compiled.append(indent * indent_count + "data[ptr] -= {}".format(abs(sum_balance)))
                    sum_balance = 0

            elif char0 in '<>':
                #This section condenses consecutive <> chars into one line of python
                if char0 == '>':
                    location_balance += 1
                else:
                    location_balance -= 1
                if char1 not in '<>' and location_balance != 0:
                    #This means that char0 is the last consecutive < or >
                    if location_balance > 0:
                        self.compiled.append(indent * indent_count + "ptr += {}".format(location_balance))
                    else:
                        self.compiled.append(indent * indent_count + "ptr -= {}".format(abs(location_balance)))
                    location_balance = 0

            elif char0 == '.':
                self.compiled.append(indent * indent_count + "print(data[ptr])")

            elif char0 == ',':
                self.compiled.append(indent * indent_count + "data[ptr] = input('Slot {}: '.format(ptr))")

            elif char0 == '[':
                self.compiled.append(indent * indent_count + "while data[ptr] != 0:")
                indent_count += 1

            elif char0 == ']':
                indent_count -= 1

            index += 1

        self.compiled = "\n".join(self.compiled)