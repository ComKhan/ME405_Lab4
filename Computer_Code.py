import serial
import numpy as np
import matplotlib.pyplot as plt
ser = serial.Serial('COM4', 115200)
while True:
    try:
        ser.flush()

        voltage = []
        time = []
        logvals = []

        while len(voltage) < 1000:
            if ser.in_waiting > 1:
                read = str(ser.readline())[2:-5]
                vals = read.split(',')
                time.append(int(vals[0])/1000)
                voltage.append(int(vals[1])/3909*3.3)
                print(read)

        plt.plot(time, voltage)
        plt.title("Voltage vs. Time")
        plt.ylabel("Voltage (V)")
        plt.xlabel("Time (s)")
        plt.show()
        logvals = list(map(lambda x: np.log(x), voltage))
        plt.plot(time,logvals)
        plt.title("Log of Voltage vs. Time")
        plt.ylabel("Log of Voltage (log(V))")
        plt.xlabel("Time (s)")
        plt.show()
        slope = (logvals[999]-logvals[0])/(time[999]-time[0])
        print(slope)
    except KeyboardInterrupt:
        break


