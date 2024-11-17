from serial import Serial
import matplotlib.pyplot as plt


#  com finder
# print(Serial.com_enumerate())
# quit()

# save this as a file
import sys

# check if the argv[1] 
file_name = sys.argv[1]
f = open(file_name, "w")

ser = Serial('COM7', 115200)

plt.ion()
fig, ax = plt.subplots()
ax.set_title('EEG')
ax.set_xlabel('Time')
ax.set_ylabel('Brain Waves Intensity')

x, y = [], []
line, = ax.plot(x, y)

width = 500

def circular_append(l, data_point):
    l.append(data_point)
    if len(l) > width:
        l.pop(0)

def as_float(s):
    try:
        return float(s)
    except:
        return 0

def parse(data):
    try:
        # print(data)
        formatted = data.decode().strip()
        vals = formatted.split(',')
        vals = list(map(as_float, vals))
    except Exception as e:
        # print(e)
        return [0,0]
    return vals


running_max = 0
i = 0
while True:
    try:
        data = parse(ser.readline())
        # print(data)

        f.write(f"{i} {data[0]}\n")
        f.flush()

        circular_append(x, i)
        circular_append(y, data[0])


        
        # running_max = max(running_max, data[0])
        
        line.set_data(x, y)

        ax.relim()
        ax.autoscale_view(True,True,True)
        # ax.set_ylim(0, running_max)

        fig.canvas.draw()
        fig.canvas.flush_events()
        i+=1
    except Exception as e:
        print(e)

        ser.close()
        f.close()
        break