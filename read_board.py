from time import sleep
import sys
import time
from start_game import scroll_options
from settings import WHITE_PAWNS, BLACK_PAWNS, WHITE_KING, WHITE_ROOK         


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




#  !! is there any case in chess where > 2 squares can change in one move
# different_squares[i] = [sq-chess-notat][ID_from][ID_to]
def check_move(prev, curr, color):
    different_squares = compare_boards(prev, curr, color)      # Different squares = [prev val][curr val]

    ## Determine what move is being made or return blank with ERROR message
    move_to,move_from = ""
    new_empty, new_full = []

    ##  if not en passant, castling, pawn promotion

    if len(different_squares) == 2:
        return check_for_pawn_pro(different_squares,color)
    elif len(different_squares) == 3:
        # check for En passent, if not then invalid
        return 'invalid'
    elif len(different_squares) == 4:
         # check for castle, if not then invalid
         return check_for_castle(different_squares, color)
    else:
        # Handle other cases
        # error
        return;





def compare_boards(prev, curr,color):
    different_squares = []

    # Check if the arrays have the same dimensions
    if len(prev) != len(curr) or len(prev[0]) != len(curr[0]):
        print("Array error ")  # Arrays have different dimensions, cannot compare

    for i in range(len(prev)):
        for j in range(len(prev[i])):
            if prev[i][j][1] != curr[i][j][1]:
                different_squares.append((prev[i][j][0], prev[i][j][1], curr[i][j][1]))
    return check_move(different_squares, color)
   
#TODO: Implement pawn pro notation
def check_for_pawn_pro(different_squares,color):

    if(different_squares[0][1] == different_squares[1][2]):
        sq_from = different_squares[0];  # notation, id_from, id_to
        sq_to = different_squares[1] ;
    elif(different_squares[0][2] == different_squares[1][1]):
        sq_from = different_squares[1] ;
        sq_to = different_squares[0];
    else:
        return 'error'
    
    if sq_from[1] in WHITE_PAWNS and '8' in sq_to[0] and color == 'white':
        # White pawn promotion
        promote_to = scroll_options("Promote", "Queen, Knight, Rook, Bishop")
        pro_char = promote_to[0].lower()
        return pro_char + str(sq_from[0][1]) + str(sq_to[0])

    elif sq_from[1] in BLACK_PAWNS and '1' in sq_to[0] and color == 'black':
        # Black pawn promotion
        promote_to = scroll_options("Promote", "Queen, Knight, Rook, Bishop")
        pro_char = promote_to[0].lower()
        return pro_char + str(sq_from[0][1]) + str(sq_to[0])
    else:
        # Normal move
        return str(sq_from[0]) + str(sq_to[0])

# notation, id_from, id_to
def check_for_castle(different_squares,color):
    king_from_pos, rook_right_from, rook_left_from, king_right_to, 
    rook_right_to, rook_left_to, king_left_to = False

    if (color == 'white'):
        for square in different_squares:  
            if square[0].lower() == 'a1' and square[1] in WHITE_ROOK:
                    rook_right_from = True;
            elif square[0].lower() == 'c1' and square[2] in WHITE_KING:
                    rook_right_to = True;
            elif square[0].lower() == 'd1' and square[2] in WHITE_ROOK:
                    king_right_to = True;
                    king_right_to_pos = square[0];
            elif square[0].lower() == 'e1' and square[1] in WHITE_KING:
                    king_from_pos = square[0];
            elif square[0].lower() == 'f1' and square[2] in WHITE_ROOK:
                    rook_left_to = True;
            elif square[0].lower() == 'g1'and  square[2] in WHITE_KING:
                    king_left_to = True;
                    king_left_to_pos = square[0];
            elif square[0].lower() == 'h1' and square[1] in WHITE_ROOK:
                    rook_left_from = True;

        if (rook_right_from and rook_right_to and king_right_to):
             return str(king_from_pos) + str(king_right_to_pos)
        elif(rook_left_from and rook_left_to and king_left_to):
             return str(king_from_pos) + str(king_left_to_pos)
        else:
             return 'invalid'
    else: #color is black
        for square in different_squares:
            if square[0].lower() == 'a8' and square[1] in WHITE_ROOK:
                    rook_right_from = True;
            elif square[0].lower() == 'c8' and square[2] in WHITE_KING:
                    rook_right_to = True;
            elif square[0].lower() == 'd8' and square[2] in WHITE_ROOK:
                    king_right_to = True;
                    king_right_to_pos = square[0];
            elif square[0].lower() == 'e8' and square[1] in WHITE_KING:
                    king_from_pos = square[0];
            elif square[0].lower() == 'f8' and square[2] in WHITE_ROOK:
                    rook_left_to = True;
            elif square[0].lower() == 'g8'and  square[2] in WHITE_KING:
                    king_left_to = True;
                    king_left_to_pos = square[0];
            elif square[0].lower() == 'h8' and square[1] in WHITE_ROOK:
                    rook_left_from = True;

        if (rook_right_from and rook_right_to and king_right_to):
             return str(king_from_pos) + str(king_right_to_pos)
        elif(rook_left_from and rook_left_to and king_left_to):
             return str(king_from_pos) + str(king_left_to_pos)
        else:
             return 'invalid'