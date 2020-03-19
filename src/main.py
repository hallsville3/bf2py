from compiler import Compiler

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
    
Cap
    An optional parameter that allows the user to cap the value of the cells
"""

optimization_level = 2


compiler = Compiler('example.bf')
compiler.compile(op_level=optimization_level, cap=0)

print(compiler.compiled)
print(compiler.log)

compiler.save('compiled.py')
