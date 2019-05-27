import sys
import random

args = sys.argv

X_MIN = 0
Y_MIN = 0
X_MAX = 100
Y_MAX = 100

if len(args) < 2:
    data_size = 10
elif len(args) == 2:
    data_size = int(args[1])
else:
    print('error')
    sys.exit(1)

with open('input.dat', 'w') as fout:
    for i in range(data_size):
        l = [str(random.uniform(0, 100)), str(random.uniform(0,100)), str(random.uniform(10000, 1000000))]
        fout.writelines(' '.join(l))
        fout.write('\n')

sys.exit(0)
