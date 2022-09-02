import matplotlib.pyplot as plt
import numpy as np
import sys

with open('scores_no_shield.txt') as f:
    w = [float(x) for x in next(f).split()][0] # read first line
    y1 = []
    for line in f: # read rest of lines
        y1.append([float(x) for x in line.split()][0])

with open('scores_shield.txt') as f:
    w = [float(x) for x in next(f).split()][0] # read first line
    y2 = []
    for line in f: # read rest of lines
        y2.append([float(x) for x in line.split()][0])

x = np.array(range(0, len(y1)))*10
print(x)
print(y1)
print(y2)
# plt.plot(x,y1)
plt.plot(x, y1, 
         marker='o', color='b')
plt.plot(x,y2, linestyle='dashed', marker='s', color='tab:orange')
plt.title("Scores during Training for Classic Pacman")
plt.ylabel("Average Rewards")
plt.xlabel("Training Episodes")
plt.legend(["W/o shield", "With shield"])
plt.grid()
plt.show()