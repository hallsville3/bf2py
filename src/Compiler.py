import re


def clean(bf):
    # Removes any non-bf characters from the given program and returns as a list
    return [char0 for char0 in bf if char0 in "+-<>.,[]"]


class Compiler(object):
    def __init__(self, bf):
        self.bf = clean(bf)
        self.compiled = None

    def compile(self, op_level = 2):
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
            chars = ["\0" if index + i >= len(self.bf) else self.bf[index + i] for i in range(10)]
            char0 = chars[0]
            char1 = chars[1]

            #Major optimizations
            if ''.join(chars[0:3]) == "[-]" and op_level > 0:
                #Sets data[ptr] to 0
                self.compiled.append(indent * indent_count + "data[ptr] = 0")
                index += 3
                continue

            elif ''.join(chars[0:3]) == "[->" and op_level > 1:

                temp_index = index
                while self.bf[temp_index] != ']':
                    temp_index += 1

                expression = ''.join(self.bf[index:temp_index + 1])

                if expression.count('<') == expression.count('>'):
                    count = expression.count('<')
                    if re.compile("\[->+\+<+\]").match(expression):
                        #[->+<]
                        self.compiled.append(indent * indent_count + "data[ptr + {}] += data[ptr]".format(count))
                        self.compiled.append(indent * indent_count + "data[ptr] = 0")
                        index += 4 + count * 2
                        continue
                    elif re.compile("\[->+-<+\]").match(expression):
                        #[->-<]
                        self.compiled.append(indent * indent_count + "data[ptr + {}] -= data[ptr]".format(count))
                        self.compiled.append(indent * indent_count + "data[ptr] = 0")
                        index += 4 + count * 2
                        continue
                    elif re.compile("\[->+\+>+\+<+\]").match(expression):
                        #[->+>+<<]
                        #First we need to count how many > there are in the first two groups
                        counts = [group.count('>') for group in re.compile(">+").findall(expression)]
                        self.compiled.append(indent * indent_count + "data[ptr + {}] += data[ptr]".format(counts[0]))
                        self.compiled.append(indent * indent_count + "data[ptr + {}] += data[ptr]".format(sum(counts)))
                        self.compiled.append(indent * indent_count + "data[ptr] = 0")
                        index += 5 + count * 2
                        continue
                    elif re.compile("\[->+->+-<+\]").match(expression):
                        #[->->-<<]
                        #First we need to count how many > there are in the first two groups
                        counts = [group.count('>') for group in re.compile(">+").findall(expression)]
                        self.compiled.append(indent * indent_count + "data[ptr + {}] -= data[ptr]".format(counts[0]))
                        self.compiled.append(indent * indent_count + "data[ptr + {}] -= data[ptr]".format(sum(counts)))
                        self.compiled.append(indent * indent_count + "data[ptr] = 0")
                        index += 5 + count * 2
                        continue

            elif ''.join(chars[0:3]) == "[-<" and op_level > 1:

                temp_index = index
                while self.bf[temp_index] != ']':
                    temp_index += 1

                expression = ''.join(self.bf[index:temp_index + 1])

                if expression.count('<') == expression.count('>'):
                    count = expression.count('<')
                    if re.compile("\[-<+\+>+\]").match(expression):
                        #[-<+>]
                        self.compiled.append(indent * indent_count + "data[ptr - {}] += data[ptr]".format(count))
                        self.compiled.append(indent * indent_count + "data[ptr] = 0")
                        index += 4 + count * 2
                        continue
                    elif re.compile("\[-<+->+\]").match(expression):
                        #[-<->]
                        self.compiled.append(indent * indent_count + "data[ptr - {}] -= data[ptr]".format(count))
                        self.compiled.append(indent * indent_count + "data[ptr] = 0")
                        index += 4 + count * 2
                        continue
                    elif re.compile("\[-<+\+<+\+>+\]").match(expression):
                        #[-<+<+>>]
                        #First we need to count how many < there are in the first two groups
                        counts = [group.count('<') for group in re.compile("<+").findall(expression)]
                        self.compiled.append(indent * indent_count + "data[ptr - {}] += data[ptr]".format(counts[0]))
                        self.compiled.append(indent * indent_count + "data[ptr - {}] += data[ptr]".format(sum(counts)))
                        self.compiled.append(indent * indent_count + "data[ptr] = 0")
                        index += 5 + count * 2
                        continue
                    elif re.compile("\[-<+-<+->+\]").match(expression):
                        #[-<-<->>]
                        #First we need to count how many < there are in the first two groups
                        counts = [group.count('<') for group in re.compile("<+").findall(expression)]
                        self.compiled.append(indent * indent_count + "data[ptr - {}] -= data[ptr]".format(counts[0]))
                        self.compiled.append(indent * indent_count + "data[ptr - {}] -= data[ptr]".format(sum(counts)))
                        self.compiled.append(indent * indent_count + "data[ptr] = 0")
                        index += 5 + count * 2
                        continue

            #Regular translation and minor optimizations
            if char0 in '+-':
                #This section condenses consecutive +- chars into one line of python
                if char0 == '+':
                    sum_balance += 1
                else:
                    sum_balance -= 1
                if char1 not in '+-' and sum_balance != 0 or op_level == 0:
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
                if char1 not in '<>' and location_balance != 0 or op_level == 0:
                    #This means that char0 is the last consecutive < or >
                    if location_balance > 0:
                        self.compiled.append(indent * indent_count + "ptr += {}".format(location_balance))
                    else:
                        self.compiled.append(indent * indent_count + "ptr -= {}".format(abs(location_balance)))
                    location_balance = 0

            elif char0 == '.':
                self.compiled.append(indent * indent_count + "print(chr(data[ptr] % 256), end='')")

            elif char0 == ',':
                self.compiled.append(indent * indent_count + "data[ptr] = input('Slot {}: '.format(ptr))")

            elif char0 == '[':
                self.compiled.append(indent * indent_count + "while data[ptr] != 0:")
                indent_count += 1

            elif char0 == ']':
                indent_count -= 1

            index += 1

        self.compiled = "\n".join(self.compiled)