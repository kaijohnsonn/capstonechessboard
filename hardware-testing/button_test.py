from gpiozero import Button
from signal import pause
import time


button1 = Button(4)  # GPIO pin 4 for Button 1
button2 = Button(17)  # GPIO pin 17 for Button 2

# Variables to keep track of button states and times
button1_state = False
button2_state = False
last_change_time = time.time()
debounce_time = 0.1

def handle_buttons():
    global button1_state, button2_state, last_change_time
    
    button1_pressed = button1.is_pressed
    button2_pressed = button2.is_pressed

    # Check if the state of Button 1 has changed
    if button1_pressed != button1_state:
        button1_state = button1_pressed
        handle_button_state(button1_state, "Button 1")

    # Check if the state of Button 2 has changed
    if button2_pressed != button2_state:
        button2_state = button2_pressed
        handle_button_state(button2_state, "Button 2")


def handle_button_state(button_state, button_name):
    global last_change_time

    # Check if enough time has passed since the last change
    if time.time() - last_change_time > debounce_time:
        # Call the button_pressed function when the button is pressed
        if button_state:
            if button_name == "Button 1":
                button1_pressed()
            elif button_name == "Button 2":
                button2_pressed()
                   
        # Update the last change time
        last_change_time = time.time()
            

def button1_pressed():
    print("Button 1 pressed!")
    
def button2_pressed():
    print("Button 2 pressed!")

# Assign the handle_buttons function to both when_pressed and when_released events
button1.when_pressed = handle_buttons 
button2.when_pressed = handle_buttons
button1.when_released = handle_buttons 
button2.when_released = handle_buttons

pause()  # This keeps the script running and listening for events
