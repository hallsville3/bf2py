data = [0] * 30000
ptr = 0

# bf2py Program Start
data[ptr] += 4
while data[ptr] != 0:
    data[ptr] -= 1
    ptr += 1
    data[ptr] += 8
    ptr -= 1
data[ptr] += 8
while data[ptr] != 0:
    ptr += 2
    data[ptr] += 8
    ptr -= 2
    data[ptr] -= 1
ptr += 2
data[ptr] += 1
ptr -= 2
data[ptr] += 8
while data[ptr] != 0:
    data[ptr] -= 1
    ptr += 3
    data[ptr] += 12
    ptr -= 3
ptr += 3
data[ptr] += 1
ptr -= 3
data[ptr] += 2
while data[ptr] != 0:
    ptr += 4
    data[ptr] += 13
    ptr -= 4
    data[ptr] -= 1
ptr += 4
while data[ptr] != 0:
    data[ptr] -= 1
    ptr -= 2
    print(chr(data[ptr] % 256), end="")
    data[ptr] += 1
    ptr += 1
    print(chr(data[ptr] % 256), end="")
    data[ptr] += 1
    ptr -= 2
    print(chr(data[ptr] % 256), end="")
    ptr += 3
