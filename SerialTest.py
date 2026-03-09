from modules.Serial_Com import *

port = "COM4"
baud = 9600
def communication():
    arduino = connect(port, baud)
    if arduino is None:
        return

    laser_on(arduino)
    laser_off(arduino)
    step_motor(arduino)
    reset_motor(arduino)
    disconnect(arduino)

if __name__ == "__main__":
    communication()