# Has not been tested yet
# Will need to change gpio pin numbers

from gpiozero import Button
from signal import pause

def button1_pressed():
    print("Button 1 pressed!")

def button2_pressed():
    print("Button 2 pressed!")

button1 = Button(4)  # GPIO pin for Button 1
button2 = Button(17)  # GPIO pin for Button 2

button1.when_pressed = button1_pressed
button2.when_pressed = button2_pressed

pause()  # This keeps the script running and listening for events