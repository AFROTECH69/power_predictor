import asyncio
import websockets
import serial
import pandas as pd
from datetime import datetime
import io

ser = serial.Serial('/dev/ttyACM0', 115200)

async def stream_data(websocket, path):
    while True:
        try:
            raw_data = ser.readline().decode('utf-8').strip()
            components = raw_data.split(',')
            if len(components) == 7:
                Process_ID, voltage, current, power, energy, frequency, pf = components
                data = {
                    "Timestamp": [datetime.now()],
                    "Station": [Process_ID],
                    "Voltage": [voltage],
                    "Current": [current],
                    "Power": [power],
                    "Energy": [energy],
                    "Frequency": [frequency],
                    "Power Factor": [pf],
                }
                df = pd.DataFrame(data)
                csv_data = df.to_csv(index=False)
                await websocket.send(csv_data)
            else:
                print(f"Invalid data format: {raw_data}")
        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(1)

start_server = websockets.serve(stream_data, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
