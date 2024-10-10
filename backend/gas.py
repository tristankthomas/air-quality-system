from fastapi import FastAPI
import serial
import threading
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
device = "ttyUSB0"

origins = [
    "http://localhost:8080",  # Allow your Vue.js app running locally
    "http://172.20.10.2:8080", # Allow your Vue.js app running on Raspberry Pi
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Open the serial port to read data from the Arduino
ser = serial.Serial(f'/dev/{device}', 9600, timeout=1)



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
        print(gas_reading)
        return {"gas": gas_reading}
    return {"message": "No gas data available yet"}
