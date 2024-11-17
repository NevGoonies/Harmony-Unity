from analyze import analyze_brainwave, get_freq
import numpy as np
import sys
from circular_queue import CircularQueue
from read_brain import real_time_read
from utils import setup_plotting
from serial import Serial
import serial.tools.list_ports
import threading
# Useful variablees

f = open("show.txt", "w")

RUNNING = 1000
SAMPLE = 300
X = CircularQueue(RUNNING)
Y = CircularQueue(RUNNING)

anxiety = CircularQueue(SAMPLE)
anxietyX = CircularQueue(SAMPLE)
anxiety2  = CircularQueue(SAMPLE)
running_average = CircularQueue(SAMPLE)
running_average_print = CircularQueue(SAMPLE)
fig, ax = setup_plotting(['Brain Waves', 'Anxiety','Anxiety (Welch)', 'Running Average'], ['Time', 'Time', 'Time','Time'], ['Intensity', 'Frequency', 'Frequency', 'Frequency'])
line, = ax[0].plot(X.data, Y.data)
line2, = ax[1].plot(X.data, anxiety.data)
line3, = ax[2].plot(X.data, anxietyX.data)
line4, = ax[3].plot(X.data, running_average.data)

fig.canvas.draw()
fig.canvas.flush_events()

def get_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description:
            return port.device
    return None

ser = Serial(get_arduino_port(), 115200)
i = 0

def read_thread():
    global i, X, Y, ax
    for data in real_time_read(ser):
        X.append(i)
        Y.append(data)
        i = i + 1
        print(data)
        
        
    # read the data
    
# start the thread
t = threading.Thread(target=read_thread)
t.start()
    # append the data to the queue
while True:
    # print(i)
    if i < SAMPLE:
        continue

    anxietyX.append(i)
    out = get_freq(Y.data[-SAMPLE:])['fft']
    welch = get_freq(Y.data[-SAMPLE:])['welch']
    anxiety.append(out)
    anxiety2.append(welch)
    running_average.append(np.mean(anxiety.data[-50:]))
    line2.set_data(anxietyX.data, anxiety.data)
    ax[1].relim()
    ax[1].autoscale_view(True,True,True)
    
    line3.set_data(anxietyX.data, anxiety2.data)
    ax[2].relim()
    ax[2].autoscale_view(True,True,True)
    
    line4.set_data(range(len(running_average.data)), running_average.data)
    ax[3].relim()
    ax[3].autoscale_view(True,True,True)

    
        
    ax[0].relim()
    ax[0].autoscale_view(True,True,True)

    line.set_data(X.data, Y.data)
    fig.canvas.draw()
    fig.canvas.flush_events()

    i+=1
    