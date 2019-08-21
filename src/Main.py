from Compiler import Compiler

"""
Sample program: +++++[->+>+<<]>>[-<<+>>]
Enters 5 into slot 0, then moves that value to slot 1 and 2
Then, moves the value back to slot 0 from slot 2, effectively copying 5 from slot 0 to 1


Output:
data = [0] * 30000
ptr = 0

#bf2py Program Start
data[ptr] += 5
data[ptr + 1] += data[ptr]
data[ptr + 2] += data[ptr]
data[ptr] = 0
ptr += 2
data[ptr - 2] += data[ptr]
data[ptr] = 0
"""

"""
Optimization Levels
    0: No Optimization
    1: Basic +- and <> Condensing and [-]
    2: Single and Double movement [->+<], [-<+>], [->-<], [-<->] and [->+>+<<], [->->-<<], [-<+<+>>], [-<-<->>]
"""

compiler = Compiler("+++++[->+>+<<]>>[-<<+>>]")
compiler.compile(op_level=2)

print compiler.compiled
