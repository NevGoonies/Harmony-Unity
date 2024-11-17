
from serial import Serial
import matplotlib.pyplot as plt

ser = Serial('COM7', 115200)
x,y = [],[]
def as_float(s):
    try:
        return float(s)
    except:
        return 0

def parse(data):
    try:
        formatted = data.decode().strip()
        vals = formatted.split(',')
        vals = list(map(as_float, vals))
    except Exception as e:
        print(e)
        return [0,0]
    return vals


while True:
    try:
        data = parse(ser.readline())
        x.append(len(x))
        y.append(data[0])
        print(data)
    except Exception as e:
        print(e)

        ser.close()
        break