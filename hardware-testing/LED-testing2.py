from gpiozero import MCP3008
import time
import RPi.GPIO as GPIO
from gpiozero import Button

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
Sig = 4
GPIOPins = [5,6,13,26]
En1 = 16
En2 = 12

button1 = Button(4) 

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIOPins, GPIO.OUT)  # Set GPIO pins 7~10 as outputs
GPIO.setup(Sig, GPIO.OUT)  # Set GPIO pin 23 as input
GPIO.setup(En1, GPIO.OUT)
GPIO.setup(En2, GPIO.OUT)
#initial_pin_state = GPIO.input(Sig)

# Initialize MCP3008 ADC on channel 0
adc = MCP3008(channel=0)

def set_pin(output_pin):
    # Function to select pin on 74HC4067
    GPIO.output(GPIOPins, control_pins[output_pin])
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
    GPIO.setup(Sig, GPIO.OUT)
    GPIO.output(Sig, initial_pin_state)
    GPIO.setup(Sig, GPIO.IN)
    
def button1_pressed():
    print("Button 1 pressed!")

def button2_pressed():
    print("Button 2 pressed!")
    
def no_press():
    katie = 1
    
def loop():
    try:
        GPIO.output(En1, 1)
        GPIO.output(En2, 0)
        
        for i in range(3):
        #set_pin(i)  # Choose an input pin on the 74HC4067
        #mux_values[i] = read_channel()  # Read the value on that pin and store in array
            if (i == 2):
                GPIO.setup(Sig, GPIO.IN)
                button1.when_pressed = button1_pressed
                button1.when_released = button1_pressed
                print(str(i))
                time.sleep(2)
            else:
                button1.when_pressed = no_press
                GPIO.setup(Sig, GPIO.OUT)
                GPIO.output(Sig, 1)
                GPIO.output(GPIOPins, control_pins[i])
                print("Not pressed" + str(i))
                time.sleep(2)


        GPIO.output(En1, 0)
        GPIO.output(En2, 1)
        
        for i in range(3):
        #set_pin(i)  # Choose an input pin on the 74HC4067
        #mux_values[i] = read_channel()  # Read the value on that pin and store in array
            if (i == 2):
                GPIO.setup(Sig, GPIO.IN)
                button1.when_pressed = button2_pressed
                button1.when_released = button2_pressed
                print(str(i))
                time.sleep(2)
            else:
                button1.when_pressed = no_press
                GPIO.setup(Sig, GPIO.OUT)
                GPIO.output(Sig, 1)
                GPIO.output(GPIOPins, control_pins[i])
                print("Not pressed" + str(i))
                time.sleep(2) 
        #restore_pin_state()

    except KeyboardInterrupt:
        # Cleanup GPIO and ADC on Ctrl+C
        GPIO.cleanup()
        adc.close()

if __name__ == "__main__":
    try:
        while True:
            loop()

    except KeyboardInterrupt:
        # Cleanup GPIO and ADC on Ctrl+C
        GPIO.cleanup()
        adc.close()
