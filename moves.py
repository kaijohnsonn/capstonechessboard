import time

# Move string is the starting position and ending position (ex. e2e4)
# Example error: HTTP 400: Bad Request: {'error': 'Piece on f8 cannot move to a2'}
def make_move(client, gameId):
    try:
        print("White time: " + str(next(client.board.stream_game_state(gameId))['state']['wtime']))
        print("Black time: " + str(next(client.board.stream_game_state(gameId))['state']['btime']))
        print("Computer move: " + next(client.board.stream_incoming_events())['game']['lastMove'])
        move = input('Your move: \n')
        client.board.make_move(gameId, move)
        time.sleep(1)
    except Exception as error:
        print(error)
        print("Invalid move")

def play_game(client, gameId):
    while len(list(client.games.get_ongoing())) > 0:
        make_move(client, gameId)
    
    print("Game over")