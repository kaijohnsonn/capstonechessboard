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
                isMyTurn = True

        if state['type'] == 'gameState':
            print("White time: " + str(state["wtime"]))
            print("Black time: " + str(state["btime"]))

            while state["status"] == "started" and isMyTurn:
                try:
                    lastPlayerMove = input('Your move: \n')
                    client.board.make_move(gameId, lastPlayerMove)
                    isMyTurn = False
                    
                except Exception as error:
                    if "HTTP 400: Bad Request: {'error': 'Not your turn, or game already over'}" in str(error):
                        print("Error: Not your turn or game already over.")
                        break
                    else:
                        print(error)

            if state["status"] != "started":
                print("Game over: " + state["status"])


# TODO
# start with white
# test invalid moves
# play against computer
