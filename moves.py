# Move string is the starting position and ending position (ex. e2e4)
# Example error: HTTP 400: Bad Request: {'error': 'Piece on f8 cannot move to a2'}
def stream_game_state(client, gameId, color):

    if color == 'black':
        isMyTurn = False
    else: isMyTurn = True

    lastPlayerMove = 'n/a'

    game_state = client.board.stream_game_state(gameId)
    for state in game_state:
        if state['type'] == 'gameFull':
            state = state['state']

        if "moves" in state:
            # Print the opponent's moves
            opponent_moves = state["moves"]
            if opponent_moves[-4:] != lastPlayerMove and opponent_moves[-4:] != '':
                print(f"Opponent's move: {opponent_moves[-4:]}")
                # light up opponents leds here
                # call function with while true for detecting button 2 press.
                # when button 2 pressed, verify move is correct
                verify_opp_move()
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
                    client.board.make_move(gameId, lastPlayerMove)
                    isMyTurn = False
                    
                except Exception as error:stream_game_state
                    if "HTTP 400: Bad Request: {'error': 'Not your turn, or game already over'}" in str(error):
                        print("Error: Not your turn or game already over.")
                        break
                    else:
                        # INVALID MOVE HANDLE
                        print(error)

            if state["status"] != "started":
                # END OF GAME HANDLING
                print("Game over: " + state["status"])
                
def verify_opp_move():
    while True:
        if but2_pressed[0]:
            but2_pressed[0] = False  # Reset the flag
            # CHECK IF THE MOVE WAS CORRECT
            break

        time.sleep(0.1)
        
def make_move_on_press():
    while True:
        if but1_pressed[0]:
            but1_pressed[0] = False  # Reset the flag
            # SEND THE MOVE HERE
            # client.board.make_move(gameId, lastPlayerMove)
            break

        time.sleep(0.1)
