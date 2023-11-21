#include all necessary packages to get LEDs to work with Raspberry Pi
import time
import board
import neopixel

#Focusing on a particular strip, use the command Fill to make it all a single colour
#based on decimal code R, G, B. Number can be anything from 255 - 0. Use an RGB Colour
#Code Chart Website to quickly identify the desired fill colour.
# pixels1.fill((0, 220, 0))

def opponentLED(move: str):
    #Initialise a strips variable, provide the GPIO Data Pin
    #utilised and the amount of LED Nodes on strip and brightness (0 to 1 value)
    pixels1 = neopixel.NeoPixel(board.D18, 300, brightness=1)

    #Below demonstrates how to individual address a colour to a LED Node, in this case
    #LED Node 10 and colour Blue was selected
    letter = move[0]
    number_from_letter = string.ascii_uppercase.index(letter) - 1
    threes = snake_matrix_value[number_from_letter,move[1]]
    pixels1[threes-2] = (225, 225, 255)
    pixels1[threes-1] = (225, 225, 255)
    pixels1[threes] = (225, 225, 255)

    #Add a brief time delay to appreciate what has happened    
    time.sleep(4)

    #Complete the script by returning all the LED to off
    pixels1.fill((0, 0, 0))

def snake_matrix_value(column, row):
    matrix = [[0,3,6,9,12,15,18,21,24,27],
          [57, 54, 51, 48, 45, 42, 39, 36, 33, 30],
          [60, 63, 66, 69, 72, 75, 78, 81, 84, 87],
          [120, 117, 114, 111, 108, 105, 102, 99, 96, 93, 90],
          [123, 126, 129, 132, 135, 138, 141, 144, 147, 150],
          [180, 177, 174, 171, 168, 165, 162, 159, 156, 153],
          [183, 186, 189, 192, 195, 198, 201, 204, 207, 210],
          [240, 237, 234, 231, 228, 225, 222, 219, 216, 213],
          [243, 246, 249, 252, 255, 258, 261, 264, 267, 270],
          [300, 297, 294, 291, 288, 285, 282, 279, 276, 273]]
    return matrix[row][column]

#%%

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