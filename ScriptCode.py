
from datetime import datetime
from gpiozero import CPUTemperature
cpu = CPUTemperature()
import serial
import sys
import csv
import time
import subprocess

Tester = sys.argv[1]

SERIAL_PORT = "/dev/serial0"  # Raspberry Pi 4

port ='/dev/ttyACM0'
GPS = serial.Serial(port)
GPS.baudrate = 9600

ser = serial.Serial(SERIAL_PORT, baudrate=115200, timeout=5)
MESSAGE = 'AT+CSQ\r'
with open(Tester + '.csv', 'w') as file:
    i = 0
    writer = csv.writer(file, delimiter=',')
    now = datetime.now()
    InitializationTime = int(now.strftime("%S"))
    print("The initialization time is:", InitializationTime)
    while((InitializationTime % 10) != 8):
        now = datetime.now()
        InitializationTime = int(now.strftime("%S"))
    start_time = time.perf_counter()
    base_time = start_time
    newtime = time.perf_counter()
    counter = 0
    while(counter < 42):
        print("readingline")
        print("Asking for RSSI")
        ser.write(MESSAGE.encode('utf-8'))  # ask for the time
        print("Listening for signal strength...")
        CSQLine = ser.readline().decode('utf-8')
        while(CSQLine.find("+CSQ:") == -1):
             CSQLine = ser.readline().decode('utf-8')

        reply2 = CSQLine
        temp = CPUTemperature()
        while((newtime - start_time) < 5):
            newtime = time.perf_counter()
            line = GPS.readline()
            loopline = line.decode('latin-1')
            #print(loopline)
            if(loopline.find("GNRMC") is not -1):
             readline=GPS.readline()
             readloopline=line.decode('latin-1')

        newline=str(readloopline)
        list=newline.split(",")
        A = list[1:7]
        print(A)
        now = datetime.now()
        writer.writerow([now.strftime("%Y-%m-%d %H:%M:%S"), reply2, str(temp), A])
        print("Data logged at", now.strftime("%Y-%m-%d %H:%M:%S"))
        counter += 1
        start_time = newtime
        print(time.perf_counter()-base_time)
    print("DONE")
    final_time = time.perf_counter() - base_time
    print("The final time to run all analysis was", final_time)
    q = subprocess.Popen(["sudo", "pkill", "-f", "gst-launch"])
    p = subprocess.Popen(["sudo", "ifconfig", "eth0", "up"])
