import numpy as np
import sys
y = []
diff = int(sys.argv[1])
with open(sys.argv[2]) as f:
    lines = f.readlines()
    w = []
    for line in lines:
        w.append(float(line))
    if diff > 0:
        print(sum(w[:-diff])/len(w[:-diff]))
    else:
        print(sum(w)/len(w))