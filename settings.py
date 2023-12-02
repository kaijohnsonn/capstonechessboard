#https://stackoverflow.com/questions/13034496/using-global-variables-between-files

global but1_pressed
but1_pressed = [False]

global but2_pressed
but2_pressed = [False]

global BINARY_IN
BINARY_IN = [
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

global CONTROL_PINS
BINARY_IN = [5,6,13,26]

global SIGNAL
SIGNAL = 8

global ENABLE
ENABLE = [12, 16, 23, 24]
   
global NUM_MUX    
NUM_MUX = 4

global NUM_RFID
NUM_RFID = 16

global SLEEP
SLEEP = 0.01
    
    
    
