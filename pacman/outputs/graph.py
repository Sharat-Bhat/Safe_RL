import matplotlib.pyplot as plt
import numpy as np
import sys
n = len(sys.argv) - 2
y = []
diff = int(sys.argv[1])
for i in range(n):
    with open(sys.argv[i+2]) as f:
        lines = f.readlines()
        y.append([])
        for j in range(len(lines)-diff+1): # read rest of lines
            y[i].append(float(lines[j]))

# with open('scores_shield.txt') as f:
#     w = [float(x) for x in next(f).split()][0] # read first line
#     y2 = []
#     for line in f: # read rest of lines
#         y2.append([float(x) for x in line.split()][0])

x = np.array(range(0, len(y[0])))*10
print(x)
for i in range(n):
    print(y[i])
# print(y2)
# plt.plot(x,y1)
plt.plot(x, y[0], 
         marker='o', color='b', label="W/o shield")
plt.plot(x,y[1], linestyle='dashed', marker='s', color='tab:orange', label="With Shield")
# plt.plot(x,y[2], linestyle='dashed', marker='d', color='k', label="Shield 4 Cross")
# plt.plot(x,y[3], marker='^', color='r', label="Shield 8 Cross")
plt.title("Scores during Training for Pacman: Grid "+sys.argv[2].split('_')[1])
plt.ylabel("Average Rewards")
plt.xlabel("Training Episodes")
# plt.legend()
plt.legend(bbox_to_anchor=(1.0, 1.2), loc='upper left')
plt.tight_layout()
plt.grid()
plt.savefig("../plots/"+ sys.argv[2].split('_')[1]+".png")   # save the figure to file
plt.show()
# plt.close(fig)