from datetime import datetime
import serial
import matplotlib.pyplot as plt
import keyboard
from matplotlib.animation import FuncAnimation
import sys

figure = plt.figure()
plt.title("Resistor temperature")
plt.xlabel("Time [-]")
plt.ylabel("Temperature [C]")
hSerial = serial.Serial('COM5', 115200, timeout=1, parity=serial.PARITY_NONE)
print("connected to: " + hSerial.portstr)

temperature_samples = []
t = []
t_value = 0
lineplot, = plt.plot_date(t, temperature_samples, '.', c='r')


def update(frame):
    hSerial.write(b't')
    hSerial.flushOutput()
    line = hSerial.read(100)
    temperature = line[31:].decode("utf-8")
    if temperature == '' and len(temperature_samples) != 0:
        temperature = temperature_samples[-1]
    print(float(temperature))
    temperature_samples.append(float(temperature))
    t.append(datetime.now())
    lineplot.set_data(t, temperature_samples)
    figure.gca().relim()
    figure.gca().autoscale_view()
    if keyboard.is_pressed('q'):
        print("Exit")
        sys.exit()
    if keyboard.is_pressed('w'):
        hSerial.write(b'w')
        answer = hSerial.read(100)
        print(answer)
    if keyboard.is_pressed('s'):
        hSerial.write(b's')
        answer = hSerial.read(100)
        print(answer)
    return lineplot,


animation = FuncAnimation(figure, update, interval=100)
plt.show()
