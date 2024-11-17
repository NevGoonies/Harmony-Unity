# this time we read the data from a file

import matplotlib.pyplot as plt
import numpy as np
import sys

width = 500

def circular_append(l, data_point):
    l.append(data_point)
    if len(l) > width:
        l.pop(0)

# check if the argv[1]
file_name = sys.argv[1]

f = open(file_name, "r")
lines = f.readlines()

x = []
y = []


plt.ion()
fig, ax = plt.subplots()
ax.set_title('EEG')
ax.set_xlabel('Time')
ax.set_ylabel('Brain Waves Intensity')
plt_line, = ax.plot(x, y)

i = 0
for line in lines:
    i += 1
    data = line.split()
    print(data)
    x.append(i)
    y.append(float(data[1]))
    # print(data)
    plt_line.set_data(x, y)

    ax.relim()
    ax.autoscale_view(True,True,True)

    fig.canvas.draw()
    fig.canvas.flush_events()

f.close()
