from leds import * 
# Move string is the starting position and ending position (ex. e2e4)
# Example error: HTTP 400: Bad Request: {'error': 'Piece on f8 cannot move to a2'}
from read_board import create_board_matrix, check_move
from verify_moves import user_make_move, verify_opp_move
from move_on_board import read_rfid
from lcds import print_lcd1, print_lcd2, clear_lcd1, clear_lcd2


def stream_game_state(client, gameId, color):

    if color == 'black':
        isMyTurn = False
    else: isMyTurn = True

    lastPlayerMove = 'n/a'

    game_state = client.board.stream_game_state(gameId)
    previous_board = read_rfid() # should read init state on an init button press

    for state in game_state:
        if state['type'] == 'gameFull':
            state = state['state']

        if "moves" in state:
            # Print the opponent's moves
            opponent_moves = state["moves"]
            if opponent_moves[-4:] != lastPlayerMove and opponent_moves[-4:] != '':
                print(f"Opponent's move: {opponent_moves[-4:]}")
                opponentLED(opponent_moves[-4:])
                # call function with while true for detecting button 2 press.
                # when button 2 pressed, verify move is correct
                flag = False

                while not flag:
                    verify, previous_board = verify_opp_move(previous_board, color, opponent_moves[-4:])
                    if not verify:
                        # DO SOMETHING
                        clear_lcd1()
                        print_lcd1('Incorrect placement:')
                        clear_lcd2()
                        print_lcd2(opponent_moves[-4:])
                    else:
                        flag = True  # Set flag to True when opp move is correct
                    
                isMyTurn = True

        if state['type'] == 'gameState':
            print("White time: " + str(state["wtime"]))
            print("Black time: " + str(state["btime"]))
            # TODO:
            # Only print the time if it is a timed game
            # Add countdown for timer!!

            while state["status"] == "started" and isMyTurn:
                try:
                    # INPUT FROM RFID HERE
                    lastPlayerMove = input('Your move: \n')
                    # MOVE MAKE MOVE FUNCTION TO BUTTON 1 PRESSED
                    lastPlayerMove, previous_board = user_make_move(previous_board, color)
                    client.board.make_move(gameId, lastPlayerMove)
                    isMyTurn = False
                    
                except Exception as error:stream_game_state
                if "HTTP 400: Bad Request: {'error': 'Not your turn, or game already over'}" in str(error):
                    print("Error: Not your turn or game already over.")
                    break
                else:
                    # INVALID MOVE HANDLE
                    incorrectMoveLED()
                    print(error)

            if state["status"] != "started":
                # END OF GAME HANDLING
                print("Game over: " + state["status"])
                
