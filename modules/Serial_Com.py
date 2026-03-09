import serial
import time

# Connect to arduino using port and baud rate
def connect(port, baud):
    # Attempts to connect to arduino using given port and baud rate
    try:
        arduino = serial.Serial(port, baud, timeout=2)
        time.sleep(2)
        print(f"Connected to Arduino on {port}")
        return arduino

    # If connection is unsuccessful, give error
    except serial.SerialException as error:
        print(f"Error connecting to Arduino: {error}")
        return None

# disconnects from arduino
def disconnect(arduino):
    arduino.close()
    print("Serial connection closed!")

def send_comm(arduino, command):
    # send specific command to arduino
    arduino.write(f"{command}\n".encode())
    response = arduino.readline().decode().strip()       # Waits for a response from Arduino

    # if no response is received
    if not response:
        print(f"Warning! No response received for command: {command}")
        return None

    print(f"Arduino responded: {response}")
    return response

def laser_on(arduino):
    return send_comm(arduino, "LASER_ON")

def laser_off(arduino):
    return send_comm(arduino, "LASER_OFF")

def step_motor(arduino):
    return send_comm(arduino, "STEP")

def reset_motor(arduino):
    return send_comm(arduino, "RESET")