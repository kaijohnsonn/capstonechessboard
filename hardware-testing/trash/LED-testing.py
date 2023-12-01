import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
# Control pins output table in array form
# See truth table on page 2 of TI 74HC4067 data sheet
# Connect 74HC4067 S0~S3 to Raspberry Pi GPIO pins 4, 17, 27, 22 respectively
# Connect 74HC4067 pin 1 to Raspberry Pi GPIO pin 23 (BCM numbering)
CONTROL_PINS = [
    [0, 0, 0, 0],
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [1, 1, 0, 0],
    [0, 0, 1, 0],
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [1, 1, 1, 0],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 0, 1],
    [1, 1, 0, 1],
    [0, 0, 1, 1],
    [1, 0, 1, 1],
    [0, 1, 1, 1],
    [1, 1, 1, 1]
]

# Number of channels to read (adjustable)
NUM_CHANNELS = 16

# Holds incoming values from 74HC4067
mux_values = [0] * NUM_CHANNELS

# Set up GPIO
#CONTROL_PIN_NUMBERS = [4, 17, 27, 22]
CONTROL_PIN_NUMBERS = [22, 27, 17, 4]
OUTPUT_PIN = 23

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CONTROL_PIN_NUMBERS, GPIO.OUT)  # Set GPIO pins 7~10 as outputs
    GPIO.setup(OUTPUT_PIN, GPIO.IN)  # Set GPIO pin 23 as input

def set_control_pins(output_pin):
    # Function to select pin on 74HC4067
    GPIO.output(CONTROL_PIN_NUMBERS, CONTROL_PINS[output_pin])

def read_channel(channel):
    # Read the value from the specified channel and return it
    return GPIO.input(OUTPUT_PIN)

def display_data():
    # Dumps captured data from array to console
    print()
    print("Values from multiplexer:")
    print("========================")
    for i in range(NUM_CHANNELS):
        print(f"Input I{i} = {mux_values[i]}")
    print("========================")

def loop():
    try:
        for i in range(min(NUM_CHANNELS, len(CONTROL_PINS))):
            set_control_pins(i)  # Choose an input pin on the 74HC4067
            mux_values[i] = read_channel(i)  # Read the value on that pin and store in array

        # Display captured data
        display_data()
        time.sleep(2)

    except KeyboardInterrupt:
        # Cleanup GPIO on Ctrl+C
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        setup_gpio()
        while True:
            loop()

    except KeyboardInterrupt:
        # Cleanup GPIO on Ctrl+C
        GPIO.cleanup()
