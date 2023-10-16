from time import sleep
import sys
import time
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
button_pins = [1, 2]  # Example GPIO pins for two buttons
global scanner_map 
from enum import Enum

class ChessPiece(Enum):
    KING = "K"
    QUEEN = "Q"
    ROOK = "R"
    BISHOP = "B"
    KNIGHT = "N"
    PAWN = "P"
    EMPTY = "E"

def main():
    #init setup/ all empty
    previous_board = create_board_matrix()
    current_board = read_rfids(scanner_map)
    while True:
        if(check_init(current_board)):
            break
        else:
            print("please fix initial board setup")

    while True:
        toggle = whoseTurn()
        
        # User button pressed 
        if (GPIO.input(button_pins[0]) == GPIO.LOW) & (whoseTurn() == 'U'):
            previous_board = on_user_button_press(previous_board)
            time.sleep(5)

        # computer button pressed 
        elif (GPIO.input(button_pins[1]) == GPIO.LOW)  & (whoseTurn() == 'O'):
            previous_board = on_other_button_press(previous_board, other_move)  
            time.sleep(5)

        # end of game
        elif gameOver():
            break

# user presses button signifying end of their turn
def on_user_button_press(previous_board):
    # print(f"Button {button_pins[0]} pressed.")  
    current_board = read_rfids()
    player_move = compare_boards(previous_board, current_board)
    make_move(player_move)
    return current_board


#user presses button signifying they made the computer/other player's move

def on_other_button_press(previous_board, other_move):
    # print(f"Button {button_pins[1]} pressed.")
    current_board = read_rfids()                                # read what user's board looks like
    player_move = compare_boards(previous_board, current_board) # check what move appears to have been made
    if (make_move(player_move) == other_move):
        return current_board
    else: 
        print("incorrectly moved other player's pieces. Please try again!")
         

def read_rfids(scanner_map):
    board_layout = create_board_matrix()
    for idx in scanner_map:
        print(f"Scanning RFID scanner {idx}...")
        try:
            id, text = SimpleMFRC522(idx).read()
            # print(f"RFID scanner {idx} - Card ID: {id}, Data: {text}")
            # !! Determine data held by rfid scanners and chips!!
            if is_valid_piece(text):
                # text should be the chess pieces code
                board_layout[idx // 8][idx % 8][1] = ChessPiece(text) in ChessPiece
        except Exception as e:
            print(f"Error reading from RFID scanner {idx}: {str(e)}")
    return board_layout

def create_board_matrix():
    board_layout = [[["" for _ in range(2)] for _ in range(8)] for _ in range(8)]
    count = 0

    for row in range(len(board_layout)):
        for fil in range(len(board_layout[row])):
            # arr[0] = square id in chess notation
            # arr[1] = empty (no pieces initialized on board)
            temp = chr(65 + fil) + str(row+1) 
            count += 1
            board_layout[row][fil][0] = temp
            board_layout[row][fil][1] = ChessPiece.EMPTY

            scanner_map[count] = temp
    return board_layout


def is_valid_piece(piece_str):
    try:
        piece_enum = ChessPiece(piece_str)
        return piece_enum in ChessPiece
    
    except ValueError:
        return False
    



def compare_boards(prev, curr):
    different_squares = []

    # Check if the arrays have the same dimensions
    if len(prev) != len(curr) or len(prev[0]) != len(curr[0]):
        print("Array error ")  # Arrays have different dimensions, cannot compare

    for i in range(len(prev)):
        for j in range(len(prev[i])):
            if prev[i][j] != curr[i][j]:
                different_squares.append((i, j, prev[i][j], curr[i][j]))
    return check_move(different_squares)


def check_init():
    ##  DETERMINE IF INITIAL BOARD SETUP IS CORRECT
    if (True):
        return True
    else:
        return False
    
def check_move():
    ## Determine what move is being made or return blank with ERROR message
    return "A4B5"
