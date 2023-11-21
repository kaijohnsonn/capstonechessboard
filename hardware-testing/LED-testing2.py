from gpiozero import MCP3008
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

# Control pins output table in array form
# See truth table on page 2 of TI 74HC4067 data sheet
# Connect 74HC4067 S0~S3 to Raspberry Pi GPIO pins 7~4 respectively
# Connect 74HC4067 pin 1 to Raspberry Pi GPIO pin 23 (BCM numbering)
control_pins = [
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

# Holds incoming values from 74HC4067
mux_values = [0] * 16

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup([4, 17, 27, 22], GPIO.OUT)  # Set GPIO pins 7~10 as outputs
GPIO.setup(23, GPIO.OUT)  # Set GPIO pin 23 as input
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
initial_pin_state = GPIO.input(23)

# Initialize MCP3008 ADC on channel 0
adc = MCP3008(channel=0)

def set_pin(output_pin):
    # Function to select pin on 74HC4067
    GPIO.output([4, 17, 27, 22], control_pins[output_pin])
    print(f"P1:{control_pins[output_pin][0]}\nP2:{control_pins[output_pin][1]}\n P3:{control_pins[output_pin][2]}\nP4:{control_pins[output_pin][3]}")

def read_channel():
    # Read the analog value from the MCP3008 ADC
    return adc.value

def display_data(output_pin):
    # Dumps captured data from array to console
    print()
    print("Values from multiplexer:")
    print("========================")
    print(f"P1:{control_pins[output_pin][0]}\nP2:{control_pins[output_pin][1]}\n P3:{control_pins[output_pin][2]}\nP4:{control_pins[output_pin][3]}")

    #for i in range(15):
    #    print(f"Input I{i} = {mux_values[i]}")
    print("========================")

def restore_pin_state():
    # Restore the initial state of the pin
    GPIO.setup(23, GPIO.OUT)
    GPIO.output(23, initial_pin_state)
    GPIO.setup(23, GPIO.IN)
    
def loop():
    try:
        GPIO.output(5, 1)
        GPIO.output(6, 0)
        for i in range(5):
        #set_pin(i)  # Choose an input pin on the 74HC4067
        #mux_values[i] = read_channel()  # Read the value on that pin and store in array
        
            GPIO.output(23, 1)
            GPIO.output([4, 17, 27, 22], control_pins[i])
       
        # Display captured data
            display_data(i)
            time.sleep(2)
            
        GPIO.output(5, 0)
        GPIO.output(6, 1)
        for i in range(5):
        #set_pin(i)  # Choose an input pin on the 74HC4067
        #mux_values[i] = read_channel()  # Read the value on that pin and store in array 
            GPIO.output(23, 1)
            GPIO.output([4, 17, 27, 22], control_pins[i])
       
        # Display captured data
            display_data(i)
            time.sleep(2)
            
        # Restore the initial state of the pin
        #restore_pin_state()

    except KeyboardInterrupt:
        # Cleanup GPIO and ADC on Ctrl+C
        GPIO.cleanup()
        adc.close()

if __name__ == "__main__":
    try:
        #while True:
        loop()

    except KeyboardInterrupt:
        # Cleanup GPIO and ADC on Ctrl+C
        GPIO.cleanup()
        adc.close()
