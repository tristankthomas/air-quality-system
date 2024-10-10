from fastapi import FastAPI
import serial
import threading

app = FastAPI()

# Open the serial port to read data from the Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# Variable to store gas readings
gas_reading = None

# Function to continuously read from the serial port
def read_gas_sensor():
    global gas_reading
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()  # Read data from Arduino
            if line:
                gas_reading = line  # Store the latest gas sensor reading
        except serial.SerialException:
            print("Serial connection issue")
            break

# Start the thread for reading sensor data
thread = threading.Thread(target=read_gas_sensor)
thread.daemon = True
thread.start()

# API route to return the gas reading
@app.get("/gas-reading")
def get_gas_reading():
    if gas_reading:
        return {"gas": gas_reading}
    return {"message": "No gas data available yet"}
