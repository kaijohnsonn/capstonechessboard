from gpiozero import Button
from signal import pause
import time
from settings import but1_pressed, but2_pressed

# With the timer block on the right side of the board, Button1 is closest to you and Button2 is further
button1 = Button(4)  # GPIO pin 4 for Button 1
button2 = Button(17)  # GPIO pin 17 for Button 2

button1_state = False
button2_state = False
debounce_time = 0.1
last_change_time = time.time()

def handle_buttons():
    global button1_state, button2_state, last_change_time

    button1_pressed = button1.is_pressed
    button2_pressed = button2.is_pressed

    # Check if the state of Button 1 has changed
    if button1_pressed != button1_state:
        button1_state = button1_pressed
        handle_buttons_helper(button1_state, "Button 1")

    # Check if the state of Button 2 has changed
    if button2_pressed != button2_state:
        button2_state = button2_pressed
        handle_buttons_helper(button2_state, "Button 2")

def handle_buttons_helper(button_state, button_name):
    global last_change_time

    # Check if enough time has passed since the last change
    if time.time() - last_change_time > debounce_time:
        
        # Call the appropriate button handler depending on which was pushed
        if button_state:
            if button_name == "Button 1":
                button1_pressed()
            elif button_name == "Button 2":
                button2_pressed()

        # Update the last change time
        last_change_time = time.time()


# Add logic for button presses here:
def button1_pressed():
    # Scroll through setup options
    # Lock in player move
    #print("Button1 pressed!")
    but1_pressed[0] = True

def button2_pressed():
    # Select a setup option
    # Lock in opponent move
    #print("Button2 pressed!")
    but2_pressed[0] = True

# Handle button behaviors on when_pressed and when_released
button1.when_pressed = handle_buttons
button1.when_released = handle_buttons
button2.when_pressed = handle_buttons
button2.when_released = handle_buttons

#pause()  # This keeps the script running and listening for events

