import serial

# Open serial port
ser = serial.Serial('/dev/ttyACM0', 115200)

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)