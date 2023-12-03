from move_on_board import read_rfid
from settings import but1_pressed, but2_pressed
from read_board import check_move

def verify_opp_move(previous_board):
    while True:
        if but2_pressed[0]:
            but2_pressed[0] = False         # Reset the flag
            current_board = read_rfid()     # Returns an 8x8 array of [sq_notation, rfid #]
            move_read = check_move(previous_board, current_board)
            return move_read

            break

        time.sleep(0.1)


