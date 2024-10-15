from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import serial
import threading
import json
from fastapi.middleware.cors import CORSMiddleware
from twilio.rest import Client
import time
import asyncio

app = FastAPI()
device = "ttyUSB0"

# Twilio setup
account_sid = 'ACf1e2638d9b882481cb81b7b232300c16'
auth_token = '72993798b297e6e1c33f2561331e153d'
twilio_client = Client(account_sid, auth_token)
twilio_phone_number = '+12029198556'
recipient_phone_number = '+61490514927'

origins = [
    "http://localhost:8080",  # Allow your Vue.js app running locally
    "http://172.20.10.2:8080",  # Allow your Vue.js app running on Raspberry Pi
    "http://192.168.0.245:8080"
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
sensor_data = None

# Function to continuously read from the serial port
def read_gas_sensor():
    global sensor_data
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()  # Read data from Arduino
            if line:
                sensor_data = line  # Store the latest sensor data
                check_gas_level(sensor_data)
        except serial.SerialException:
            print("Serial connection issue")
            break

def check_gas_level(sensor_data):
    try:
        data_json = json.loads(sensor_data)
        gas_level = int(data_json.get("gas", 0))  # Adjust this key to match your data structure
        if gas_level > 800:
            #make_twilio_call()  # Trigger Twilio call
            #asyncio.create_task(notify_alerts("Warning! Gas levels are too high!"))  # Send alert notification
            #time.sleep(300)  # Sleep for 5 minutes
            print("Phone Call\n")
    except json.JSONDecodeError:
        print("Error decoding JSON from sensor")

def make_twilio_call():
    call = twilio_client.calls.create(
        twiml='<Response><Say>Warning! Gas levels are too high. Please check immediately!</Say></Response>',
        to=recipient_phone_number,
        from_=twilio_phone_number
    )
    print(f"Call initiated: {call.sid}")

# Start the thread for reading sensor data
thread = threading.Thread(target=read_gas_sensor)
thread.daemon = True
thread.start()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_alert(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
            print(f"Message sent to: {connection.client}")


manager = ConnectionManager()  # Instance of ConnectionManager to manage WebSocket connections

# Notify all connected WebSocket clients when a call is made
async def notify_alerts(message: str):
    await manager.send_alert(message)
    print("Alert notification sent.")

# WebSocket route for alert notifications
@app.websocket("/ws/alerts")
async def websocket_alerts_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    print("CONNECTED\n")
    try:
        while True:
            await manager.send_alert("Warning! Gas levels are too high!")
            await asyncio.sleep(2)  # Keep the connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# API route to return the latest sensor data
@app.get("/gas-reading")
def get_gas_reading():
    if sensor_data:
        print(sensor_data)
        return {"data": json.loads(sensor_data)}  # Return the parsed JSON data
    return {"message": "No sensor data available yet"}

