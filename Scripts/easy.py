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
import socket
import time
import os
from tqdm import tqdm

def find_arduino_serial_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description:
            return port.device
    return None

ser = False
sock = False


RUNNING = 1000
SAMPLE = 300
HEADLESS = True


X = CircularQueue(RUNNING)
Y = CircularQueue(RUNNING)

anxiety = CircularQueue(SAMPLE)
anxietyX = CircularQueue(SAMPLE)
anxiety2  = CircularQueue(SAMPLE)
running_average = CircularQueue(SAMPLE)
running_average_print = CircularQueue(SAMPLE)


p_bar = tqdm(range(10))

i = 0
def read_thread():
    global i, X, Y, ax
    for data in real_time_read(ser):
        X.append(i)
        Y.append(data)
        i = i + 1
        # print(i)
        p_bar.update(i)
        p_bar.refresh()
        if not HEADLESS:
            if line:
                line.set_data(X.data, Y.data)
            

line = False 
line2 = False
line3 = False  
line4 = False
ax = []
def main():
    global ser, sock,i 
    global line, line2, line3, line4, ax
    if not HEADLESS:
        fig, ax = setup_plotting(['Brain Waves', 'Anxiety','Anxiety (Welch)', 'Running Average'], ['Time', 'Time', 'Time','Time'], ['Intensity', 'Frequency', 'Frequency', 'Frequency'])
        line, = ax[0].plot([],[])
        line2, = ax[1].plot([],[])
        line3, = ax[2].plot([],[])
        line4, = ax[3].plot([],[])

        fig.canvas.draw()
        fig.canvas.flush_events()


    while True:
        if i < SAMPLE:
            threading.Event().wait(1)
            continue

        anxietyX.append(i)
        out = get_freq(Y.data[-SAMPLE:])['fft']
        welch = get_freq(Y.data[-SAMPLE:])['welch']
        anxiety.append(out)
        anxiety2.append(welch)
        running_average.append(np.mean(anxiety.data[-50:]))

        try:
            file = open("show.txt", "w")
            data = f"{running_average.data[-1]}\n"
            file.write(data)
            file.flush()
            file.close()
        except Exception as e:
            print(e)

        if not HEADLESS:
            
            ax[0].relim()
            ax[0].autoscale_view(True,True,True)
            line2.set_data(range(len(anxiety.data)), anxiety.data)
            ax[1].relim()
            ax[1].autoscale_view(True,True,True)
            
            line3.set_data(range(len(anxiety2.data)), anxiety2.data)
            ax[2].relim()
            ax[2].autoscale_view(True,True,True)
            
            line4.set_data(range(len(running_average.data)), running_average.data)
            ax[3].relim()
            ax[3].autoscale_view(True,True,True)

            fig.canvas.draw()
            fig.canvas.flush_events()
        threading.Event().wait(1)


if __name__ == '__main__':
    try:
        
        arduino_port = find_arduino_serial_port()

        print("Connecting to Arduino on port: ", arduino_port)

        ser = Serial(arduino_port, 115200)
        t = threading.Thread(target=read_thread)
        t.start()
        # t.join()
        main()
        # t.join()
        # t2 = threading.Thread(target=main)
        # t2.start()
        # t2.join()
    except Exception as e:
        print(e)
        ser.close()