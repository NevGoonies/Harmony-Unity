from serial import Serial
import matplotlib.pyplot as plt

def as_float(s):
    try:
        return float(s)
    except:
        return 0

def parse(data):
    try:
        # print(data)
        formatted = data.decode().strip()
        # vals = formatted.split(',')
        vals = as_float(formatted)
    except Exception as e:
        # // this rarely happens
        return 0
    return vals


# ser = Serial('COM7', 115200)

def real_time_read(ser):

    while True:
        yield parse(ser.readline())
    
    ser.close()
    