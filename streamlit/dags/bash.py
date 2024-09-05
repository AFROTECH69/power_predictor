import serial
import csv
import time

# Set up the serial connection to the Arduino
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)  # Adjust this to your serial port
ser.flush()


# Open or create the CSV file
with open('sensor_data.csv', mode='a') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Process_ID','ID', 'Timestamp', 'Voltage', 'Current', 'Power', 'Energy', 'Frequency', 'PF'])
    
    data_id = 1  # Starting ID
    station_id = 'Staition01'

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            data = line.split(',')
            
            if len(data) == 6:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                row = [station_id,data_id, timestamp] + data
                writer.writerow(row)
                print(row)
                
                data_id += 1
                station_id = 'Staition01'

            time.sleep(1)  # Delay for 1 second before next read