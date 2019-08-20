from Compiler import Compiler

"""
Sample program: +++++[->>+<<]
Enters 5 into slot 0, then moves that value to slot 2, erasing slot 0

Output:
data = [0] * 30000
ptr = 0

#bf2py Program Start
data[ptr] += 5
while data[ptr] != 0:
    data[ptr] -= 1
    ptr += 2
    data[ptr] += 1
    ptr -= 2
"""

compiler = Compiler("+++++[->>+<<]")
compiler.compile()

print compiler.compiled
