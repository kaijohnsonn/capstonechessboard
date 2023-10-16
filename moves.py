import time

# Move string is the starting position and ending position (ex. e2e4)
# Example error: HTTP 400: Bad Request: {'error': 'Piece on f8 cannot move to a2'}
def make_move(client, gameId, player_last_move):

    time.sleep(1.5)
    for event in client.board.stream_incoming_events():

        stream_last_move = event['game']['lastMove']
        color = event['game']['color']

        if stream_last_move != player_last_move and stream_last_move != '' or (stream_last_move == '' and color == 'white'):
            try:
                print("White time: " + str(next(client.board.stream_game_state(gameId))['state']['wtime']))
                print("Black time: " + str(next(client.board.stream_game_state(gameId))['state']['btime']))
                print("Opponent move: " + stream_last_move)
                move = input('Your move: \n')
                client.board.make_move(gameId, move)
                
                return move
            except Exception as error:
                print(error)
                print("Invalid move")
                return player_last_move
        
        else:
            return player_last_move

def play_game(client, gameId):
    player_last_move = "n/a"
    while len(list(client.games.get_ongoing())) > 0:
        player_last_move = make_move(client, gameId, player_last_move)
    
    print("Game over")