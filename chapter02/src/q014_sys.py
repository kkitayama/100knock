
import sys
data_path = 'data/popular-names.txt'

N = int(sys.argv[1])

with open(data_path, 'r') as f:
    for i, line in enumerate(f):
        if i == N:
            break
        print(line, end='')