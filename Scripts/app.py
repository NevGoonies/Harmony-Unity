from analyze import analyze_brainwave, get_freq
import numpy as np
import sys
from circular_queue import CircularQueue
from read_brain import real_time_read
from utils import setup_plotting
from serial import Serial
import serial.tools.list_ports

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

import threading
# Useful variablees
def find_arduino_serial_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description:
            return port.device
    return None

RUNNING = 1000
SAMPLE = 300

STOP = False

X = CircularQueue(RUNNING)
Y = CircularQueue(RUNNING)

anxiety = CircularQueue(SAMPLE)
anxietyX = CircularQueue(SAMPLE)
anxiety2  = CircularQueue(SAMPLE)
running_average = CircularQueue(SAMPLE)
running_average_print = CircularQueue(SAMPLE)

arduino_port = find_arduino_serial_port()
print(arduino_port)

ser = Serial(arduino_port, 115200)

i = 0
def read_thread():
    global i, X, Y, ax, STOP
    for data in real_time_read(ser):
        print(data)
        if STOP:
            break
        try:
            X.append(i)
            Y.append(data)
            i = i + 1
            if i%10000 == 0:
                print("Data read at index: ", i)
        except Exception as e:
            print(e)
    # read the data
    
# start the thread
t = threading.Thread(target=read_thread)
t.start()


last_running_average = 0

def analyze_thread():
    global i, X, Y, ax, STOP
    while True:
        if STOP:
            break
        
        if (i+1)%10000 == 0:
            print("Analyze thread at index: ", i)
        if i < SAMPLE:
            continue

        anxietyX.append(i)
        out = get_freq(Y.data[-SAMPLE:])['fft']
        welch = get_freq(Y.data[-SAMPLE:])['welch']
        anxiety.append(out)
        anxiety2.append(welch)
        running_average.append(np.mean(anxiety.data[-50:]))
        
        last_running_average = running_average.data[-1]

        i+=1


t2 = threading.Thread(target=analyze_thread)
t2.start()

@app.route('/')
def index():
    return 'Hello World!'

# return a json object
@app.route('/get_running_average')
def get_running_average():
    return json.dumps({'running_average': last_running_average})

if __name__ == '__main__':
    try:
        app.run(debug=True)
        # STOP = True
    except Exception as e:
        print(e)
        STOP = True