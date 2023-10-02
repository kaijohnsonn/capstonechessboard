from start_game import *
from LIChessAPI import *
from moves import *

# TODO: 
# Get inputs to start the game from the board
# Get a list of friends to choose from to start the game against

client = establish_connection()

create_game_ai(client)
#create_game_friend(client)

try:
    # this only plays the first active game
    gameId = client.games.get_ongoing()[0]['gameId']
    play_game(client, gameId)
except:
    print("No ongoing game")