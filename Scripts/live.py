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

i = 0
def read_thread():
    global i, X, Y, ax
    for data in real_time_read(ser):
        X.append(i)
        Y.append(data)
        i = i + 1
        print(i)
        if not HEADLESS:
            line.set_data(X.data, Y.data)
            
            ax[0].relim()
            ax[0].autoscale_view(True,True,True)
            
def main():
    global ser, sock,i 

    host, port = "127.0.0.1", 25001
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if not HEADLESS:
        fig, ax = setup_plotting(['Brain Waves', 'Anxiety','Anxiety (Welch)', 'Running Average'], ['Time', 'Time', 'Time','Time'], ['Intensity', 'Frequency', 'Frequency', 'Frequency'])
        line, = ax[0].plot(X.data, Y.data)
        line2, = ax[1].plot(X.data, anxiety.data)
        line3, = ax[2].plot(X.data, anxietyX.data)
        line4, = ax[3].plot(X.data, running_average.data)

        fig.canvas.draw()
        fig.canvas.flush_events()


    sock.connect((host, port))
    # start the thread
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

        data = f"{running_average.data[-1]}"
        sock.sendall(data.encode("utf-8"))
        
        if not HEADLESS:
            line2.set_data(anxietyX.data, anxiety.data)
            ax[1].relim()
            ax[1].autoscale_view(True,True,True)
            
            line3.set_data(anxietyX.data, anxiety2.data)
            ax[2].relim()
            ax[2].autoscale_view(True,True,True)
            
            line4.set_data(range(len(running_average.data)), running_average.data)
            ax[3].relim()
            ax[3].autoscale_view(True,True,True)

            fig.canvas.draw()
            fig.canvas.flush_events()
        else:
            time.sleep(5)

        i+=1

if __name__ == '__main__':
    try:
        
        arduino_port = find_arduino_serial_port()

        print("Connecting to Arduino on port: ", arduino_port)

        ser = Serial(arduino_port, 115200)
        t = threading.Thread(target=read_thread)
        t.start()

        main_thread = threading.Thread(target=main)
        main_thread.start()
    except Exception as e:
        print(e)
        ser.close()
        sock.close()