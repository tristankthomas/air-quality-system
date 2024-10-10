import serial

# Open the serial port (adjust the port based on your setup, e.g., '/dev/ttyUSB0')
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

while True:
    try:
        line = ser.readline().decode('utf-8').strip()  # Read data from Arduino
        if line:
            print(line)  # Print the data received from the Arduino
    except KeyboardInterrupt:
        print("Program stopped")
        break
