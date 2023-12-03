from time import sleep
import sys
import time
from settings import WHITE_PAWNS, BLACK_PAWNS         


def create_board_matrix():
    board_layout = [[["" for _ in range(2)] for _ in range(8)] for _ in range(8)]
    count = 0

    for row in range(len(board_layout)):
        for col in range(len(board_layout[row])):
            # arr[0] = square id in chess notation
            # arr[1] = 0 (no pieces initialized on board)
            temp = chr(65 + col) + str(row+1) 
            count += 1
            board_layout[row][col][0] = temp
            board_layout[row][col][1] = 0

    return board_layout
    

def compare_boards(prev, curr):
    different_squares = []

    # Check if the arrays have the same dimensions
    if len(prev) != len(curr) or len(prev[0]) != len(curr[0]):
        print("Array error ")  # Arrays have different dimensions, cannot compare

    for i in range(len(prev)):
        for j in range(len(prev[i])):
            if prev[i][j][1] != curr[i][j][1]:
                different_squares.append((prev[i][j][0], prev[i][j][1], curr[i][j][1]))
    return check_move(different_squares)



#  !! is there any case in chess where > 2 squares can change in one move
# different_squares[i] = [sq-chess-notat][ID_from][ID_to]
def check_move(prev, curr):
    different_squares = compare_boards(prev, curr)      # Different squares = [prev val][curr val]

    ## Determine what move is being made or return blank with ERROR message
    move_to,move_from = ""
    new_empty, new_full = []

    ##  if not en passant, castling, pawn promotion

    if len(different_squares) == 2:
        check_for_pawn_pro(different_squares)
    elif len(different_squares) == 3:
        # check for En passent, if not then invalid
    elif len(different_squares) == 4:
         # check for castle, if not then invalid
    else:
        # Handle other cases
        # error
        return;
   
#TODO: Implement pawn pro notation
def check_for_pawn_pro(different_squares):
    sq_one = different_squares[0]      # notation, id_from, id_to
    sq_two = different_squares[1]        # otation, id_from, id_to

    if(sq_one[1] == sq_two[2]):
        if (sq_one[1] in WHITE_PAWNS and '8' in sq_two[0]):
            # white pawn promotion  
            return;    
        elif (sq_one[1] in BLACK_PAWNS and '1' in sq_two[0]):
            #black pawn promotion
            return;
        else:
            # normal move
            return str(different_squares[0][0]) + str(different_squares[1][0])
    if(sq_one[2] == sq_two[1]):
        if (sq_two[1] in WHITE_PAWNS and '8' in sq_one[0]):
            # hite pawn promotion  
            return;    
        elif (sq_two[1] in BLACK_PAWNS and '1' in sq_one[0]):
            #black pawn promotion
            return;
        else:
            # normal move
            return str(different_squares[0][0]) + str(different_squares[1][0])
    else:
        return 'error'