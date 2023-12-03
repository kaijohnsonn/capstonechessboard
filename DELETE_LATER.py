class ChessPiece(Enum):
    KING_W = "K", "W"
    QUEEN_W = "Q", "W"
    ROOK_W = "R", "W"
    BISHOP_W = "B", "W"
    KNIGHT_W = "N", "W"
    PAWN_W = "P", "W"
    EMPTY = "E" , "X"
    KING_B = "K", "B"
    QUEEN_B = "Q", "B"
    ROOK_B = "R", "B"
    BISHOP_B = "B", "B"
    KNIGHT_B = "N", "B"
    PAWN_B = "P", "B"

    def __init__(self, type, color):
        self.type = type
        self.colo = color

def main():
    #init setup/ all empty
    previous_board = create_board_matrix()
    current_board = read_rfids(scanner_map)

# user presses button signifying end of their turn
def on_user_button_press(previous_board):
    # print(f"Button {button_pins[0]} pressed.")  
    current_board = read_rfids()
    player_move = compare_boards(previous_board, current_board)
    make_move(player_move)
    return current_board


#user presses button signifying they made the computer/other player's move

def on_oponent_button_press(previous_board, other_move):
    # print(f"Button {button_pins[1]} pressed.")
    current_board = read_rfids()                                # read what user's board looks like
    player_move = compare_boards(previous_board, current_board) # check what move appears to have been made
    if (make_move(player_move) == other_move):
        return current_board
    else: 
        print("incorrectly moved other player's pieces. Please try again!")



if(sq_one[1] == sq_two[2]):
        if (sq_one[1] in WHITE_PAWNS and '8' in sq_two[0]):
            # white pawn promotion  
            return;    
        elif (sq_one[1] in BLACK_PAWNS and '1' in sq_two[0]):
            #black pawn promotion
            return;
        else:
            # normal move
            return str(sq_one[0]) + str(sq_two[0])
        

    if(sq_one[2] == sq_two[1]):
        if (sq_two[1] in WHITE_PAWNS and '8' in sq_one[0] and color == 'white'):
            #white pawn promotion
            promote_to = scroll_options("Promote", "Queen, Knight, Rook, Bishop")
            pro_char = promote_to[0].lower()
            return (pro_char + str(sq_two[0][1]) + str(sq_one[0]))
 
        elif (sq_two[1] in BLACK_PAWNS and '1' in sq_one[0] and color == 'black'):
            #black pawn promotion
            promote_to = scroll_options("Promote", "Queen, Knight, Rook, Bishop")
            pro_char = promote_to[0].lower()
            return (pro_char + str(sq_two[0][1]) + str(sq_one[0]))
        else:
            # normal move
            return str(sq_two[0]) + str(sq_one[0])
    else:
        return 'error'