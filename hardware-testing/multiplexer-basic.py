#translated from http://adam-meyer.com/arduino/CD74HC4067
import RPi.GPIO as GPIO
import time

# Mux control pins
s0 = 8
s1 = 9
s2 = 10
s3 = 11

# Mux in "SIG" pin
SIG_pin = 0

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(s0, GPIO.OUT)
    GPIO.setup(s1, GPIO.OUT)
    GPIO.setup(s2, GPIO.OUT)
    GPIO.setup(s3, GPIO.OUT)

    GPIO.output(s0, GPIO.LOW)
    GPIO.output(s1, GPIO.LOW)
    GPIO.output(s2, GPIO.LOW)
    GPIO.output(s3, GPIO.LOW)

def read_mux(channel):
    control_pins = [s0, s1, s2, s3]

    mux_channel = [
        [0, 0, 0, 0],  # channel 0
        [1, 0, 0, 0],  # channel 1
        [0, 1, 0, 0],  # channel 2
        [1, 1, 0, 0],  # channel 3
        [0, 0, 1, 0],  # channel 4
        [1, 0, 1, 0],  # channel 5
        [0, 1, 1, 0],  # channel 6
        [1, 1, 1, 0],  # channel 7
        [0, 0, 0, 1],  # channel 8
        [1, 0, 0, 1],  # channel 9
        [0, 1, 0, 1],  # channel 10
        [1, 1, 0, 1],  # channel 11
        [0, 0, 1, 1],  # channel 12
        [1, 0, 1, 1],  # channel 13
        [0, 1, 1, 1],  # channel 14
        [1, 1, 1, 1]   # channel 15
    ]

    # loop through the 4 sig
    for i in range(4):
        GPIO.output(control_pins[i], mux_channel[channel][i])

    # read the value at the SIG pin
    val = analog_read(SIG_pin)

    return val

def analog_read(pin):
    # Implement analog reading here based on your specific Raspberry Pi setup
    # For example, you can use the GPIO library to read from an ADC connected to the SIG_pin
    # Replace this with your actual analog reading code
    return 0

def main():
    setup()
    try:
        while True:
            # Loop through and read all 16 values
            for i in range(16):
                print("Value at channel {} is: {}".format(i, read_mux(i)))
                time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
