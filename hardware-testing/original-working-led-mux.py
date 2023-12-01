from gpiozero import MCP3008
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

# conrol pins rep binary logic 0-15 representing each GPIO on mux
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
GPIO.setup([5,6,13,26], GPIO.OUT)  # Set GPIO pins 7~10 as outputs
GPIO.setup(8, GPIO.OUT)  # Set GPIO pin 23 as output to write to LEDs
GPIO.setup(12, GPIO.OUT)   # Set up 5 as the first enable pin
GPIO.setup(16, GPIO.OUT)   # set up 6 as the second enable pin

# Initialize MCP3008 ADC on channel 0
adc = MCP3008(channel=0)

#not calling in this version
def set_pin(output_pin):
    # Function to select pin on 74HC4067
    GPIO.output([5,6,13,26], control_pins[output_pin])
    print(f"P1:{control_pins[output_pin][0]}\nP2:{control_pins[output_pin][1]}\n P3:{control_pins[output_pin][2]}\nP4:{control_pins[output_pin][3]}")

# not sure exactly where this val comes from (will look up)
def read_channel():
    # Read the analog value from the MCP3008 ADC
    return adc.value

def display_data(output_pin):
    # Dumps captured data from array to console
    print()
    print("Values from multiplexer:")
    print("========================")
    # prints which pin is read from
    print(f"P1:{control_pins[output_pin][0]}\nP2:{control_pins[output_pin][1]}\n P3:{control_pins[output_pin][2]}\nP4:{control_pins[output_pin][3]}")

    # prints range of mux vals that will be read into as data container
    # for i in range(15):
    #    print(f"Input I{i} = {mux_values[i]}")
    print("========================")
def set_all_high():
    # Set all control pins to logic high
    for pin in range(4):
        GPIO.output([5, 6, 13, 26], 1)
   
def loop():
    try:
        #enable mux at pin 6, disable mux at pin 5
        GPIO.output(12, 1)
        GPIO.output(16, 0)
        set_all_high()
        for i in range(5):
        #set_pin(i)  # Choose an input pin on the 74HC4067
        #mux_values[i] = read_channel()  # Read the value on that pin and store in array
            #enable read out pin and select desired mux pin  through interation
            GPIO.output(8, 1)
            GPIO.output([5,6,13,26], control_pins[i])
       
            #display_data(i)     # Display captured data on mux
            time.sleep(1)
            
        #enable mux at pin 5, disable mux at pin 6
        GPIO.output(12, 0)
        GPIO.output(16, 1)
        set_all_high()
        for i in range(5):
        #set_pin(i)  # Choose an input pin on the 74HC4067
        #mux_values[i] = read_channel()  # Read the value on that pin and store in array 
             #enable read out pin and select desired mux pin  through interation
            GPIO.output(8, 1)
            GPIO.output([5,6,13,26], control_pins[i])
       
        # Display captured data
            #display_data(i)
            time.sleep(1)
            
        # Restore the initial state of the pin
        #restore_pin_state()

    except KeyboardInterrupt:
        # Cleanup GPIO and ADC on Ctrl+C
        GPIO.cleanup()
        adc.close()

if __name__ == "__main__":
    try:
        # continue looping undil Ctrl+C
        while True:
            loop()

    except KeyboardInterrupt:
        # Cleanup GPIO and ADC on Ctrl+C
        GPIO.cleanup()
        adc.close()