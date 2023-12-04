#include all necessary packages to get LEDs to work with Raspberry Pi
import time
import string
import board
import neopixel

#Focusing on a particular strip, use the command Fill to make it all a single colour
#based on decimal code R, G, B. Number can be anything from 255 - 0. Use an RGB Colour
#Code Chart Website to quickly identify the desired fill colour.
# pixels1.fill((0, 220, 0))
pixels1 = neopixel.NeoPixel(board.D18, 300, brightness=1)

def incorrectMoveLED():
    pixels1 = neopixel.NeoPixel(board.D18, 300, brightness=1)
    pixels1.fill((220, 0, 0))
    
    #Add a brief time delay to appreciate what has happened    
    time.sleep(5)

    #Complete the script by returning all the LED to off
    pixels1.fill((0, 0, 0))

#%%
def opponentLED(move: str): # 5e6b -> e6e6
    if move[0].isdigit():
        move: str = move[1::-1] + move[1:3]

    print("LEDs were called")
    lightUpLED(move[:2])
    lightUpLED(move[-2:])

    #Add a brief time delay to appreciate what has happened    
    #time.sleep(5)

    #Complete the script by returning all the LED to off
    #pixels1.fill((0, 0, 0))
#%%
def off():
    pixels1.fill((0, 0, 0))
    
def lightUpLED(move: str):
    print("LEDs small were called")
    #Initialise a strips variable, provide the GPIO Data Pin
    #utilised and the amount of LED Nodes on strip and brightness (0 to 1 value)
    # pixels1 = neopixel.NeoPixel(board.D18, 300, brightness=1)

    #Below demonstrates how to individual address a colour to a LED Node, in this case
    #LED Node 10 and colour Blue was selected
    letter = move[0]
    number_from_letter = string.ascii_lowercase.index(letter)
    threes = snake_matrix_value(int(number_from_letter),int(move[-1:]) - 1)
    pixels1[threes-2] = (225, 225, 255)
    pixels1[threes-1] = (225, 225, 255)
    pixels1[threes] = (225, 225, 255)

def snake_matrix_value(column, row):
    print(str(column) + " " + str(row))
    matrix = [[236,233,230,227,224,221,218,215,0,0],
          [185, 188, 191, 194, 197, 200, 203, 206, 0, 0],
          [176, 173, 170, 167, 164, 161, 158, 155, 0, 0],
          [125, 128, 131, 134, 137, 140, 143, 146, 0, 0],
          [116, 113, 110, 107, 104, 101, 98, 95, 0, 0],
          [65, 68, 71, 74, 77, 80, 83, 86, 0, 0],
          [56, 53, 50, 47, 44, 41, 38, 35, 0, 0],
          [5, 8, 11, 14, 17, 20, 23, 26, 0, 0]]
    return matrix[column][row]

#opponentLED("e2e4")


def snake_traverse_increment(matrix):
    result = []
    rows, cols = len(matrix), len(matrix[0])
    counter = 0
    
    for col in range(cols - 1, -1, -1):
        if (cols - 1 - col) % 2 == 0:
            # If the column index is even, traverse upwards
            for row in range(rows - 1, -1, -1):
                result.append(matrix[row][col])
                counter += 1
                if counter % 3 == 0:
                    # Increment to the next matrix element every three iterations
                    col -= 1
        else:
            # If the column index is odd, traverse downwards
            for row in range(rows):
                result.append(matrix[row][col])
                counter += 1
                if counter % 3 == 0:
                    # Increment to the next matrix element every three iterations
                    col -= 1
    
    return result
