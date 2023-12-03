from move_on_board import read_rfid
from settings import but1_pressed, but2_pressed
from read_board import check_user_move, check_opp_move
from lcds import print_lcd1, print_lcd2, clear_lcd1, clear_lcd2
import time

def verify_opp_move(previous_board, color, opp_move):
    while True:
        if but2_pressed[0]:
            but2_pressed[0] = False         # Reset the flag
            current_board = read_rfid()     # Returns an 8x8 array of [sq_notation, rfid #]
            move_read = check_opp_move(previous_board, current_board, color)
            
            if(move_read == opp_move):
                return True
            elif(opp_move[3].isdigit() and move_read[:3] == opp_move[:3]):
                return True
            break

        time.sleep(0.1)

def user_make_move(previous_board, color):
     while True:
        if but1_pressed[0]:
            but1_pressed[0] = False         # Reset the flag
            current_board = read_rfid()     # Returns an 8x8 array of [sq_notation, rfid #]
            move_read = check_user_move(previous_board, current_board, color)
            previous_board = current_board
            return move_read, previous_board

        time.sleep(0.1)

def lcd_pawn_promotion(piece):
    clear_lcd1()
    clear_lcd2()
    print_lcd1('Promoted pawn to:')

    if piece == 'q':
        print_lcd2('Queen')
    elif piece == 'r':
        print_lcd2('Rook')
    elif piece == 'b':
        print_lcd2('Bishop')
    elif piece == 'n':
        print_lcd2('Knight')