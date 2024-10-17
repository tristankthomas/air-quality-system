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

# allows requests from these addresses (CORS bypass)
origins = [
    "http://localhost:8080",
    "http://172.20.10.2:8080",
    "http://192.168.0.245:8080",
    "http://172.20.10.3:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow all methods
    allow_headers=["*"],  # allow all headers
)

ser = serial.Serial(f'/dev/{device}', 9600, timeout=1)

sensor_data = None
GAS_THRESHOLD = 200

# Reads sensor data from the serial port
def read_sensors():
    global sensor_data
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                sensor_data = line
                check_gas_level(sensor_data)
        except serial.SerialException:
            print("Serial connection issue")
            break

loop = asyncio.get_event_loop()
alert_sent = False # used to limit the number of calls 

def check_gas_level(sensor_data):
    global alert_sent
    try:
        data_json = json.loads(sensor_data)
        gas_level = int(data_json.get("gas", 0))
        # checks if gas level is too high and makes phone call if so
        if gas_level >= GAS_THRESHOLD:
            if not alert_sent:
                make_twilio_call()
                alert_sent = True
            # sends message to frontend
            asyncio.run_coroutine_threadsafe(notify_alerts("Warning! Gas levels are too high! Calling emergency contact.", "#FF0000"), loop)
        else:
            if alert_sent:
                alert_sent = False
            # sends message to frontend
            asyncio.run_coroutine_threadsafe(notify_alerts("Gas is at a safe level!", "#42b983"), loop)
    except json.JSONDecodeError:
        print("Error decoding JSON from sensor")


def make_twilio_call():
    # makes phone call using Twilio API using automated voice
    call = twilio_client.calls.create(
        twiml='<Response><Say>Warning! Gas levels are too high. Please check immediately!</Say></Response>',
        to=recipient_phone_number,
        from_=twilio_phone_number
    )
    print(f"Call initiated: {call.sid}")

# start thread for reading sensor data
thread = threading.Thread(target=read_sensors)
thread.daemon = True
thread.start()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # this is to limit websocket connections for demo purposes
        if self.active_connections:
            last_connection = self.active_connections[-1]
            self.active_connections.remove(last_connection)
            print("Removed last connection:", str(last_connection))

        await websocket.accept()
        self.active_connections.append(websocket)
        print("Active connections:", [str(conn) for conn in self.active_connections])

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_alert(self, message: str, colour: str):
        message_data = {
            "data": message,
            "colour": colour
        }
        # sends alert to all clients
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message_data))

manager = ConnectionManager()

# notify all connected WebSocket clients when a call is made
async def notify_alerts(message: str, colour: str):
    await manager.send_alert(message, colour)
    print("Alert notification sent.")



# WebSocket route for alert notifications
@app.websocket("/ws/alerts")
async def websocket_alerts_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# API route to return the latest sensor data
@app.get("/sensor-readings")
def get_gas_reading():
    if sensor_data:
        print(sensor_data)
        return {"data": json.loads(sensor_data)}
    return {"message": "No sensor data available yet"}

