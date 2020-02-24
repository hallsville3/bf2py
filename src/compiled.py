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
