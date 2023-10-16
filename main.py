import time
from start_game import *
from LIChessAPI import *
from moves import *

# TODO: 
# Get inputs to start the game from the board
# Get a list of friends to choose from to start the game against

client = establish_connection()

#create_game_ai(client)
create_game_friend(client)

friend_game_start = 0

# this allows time for the friend to accept the game
while friend_game_start == 0:
    try:
        client.games.get_ongoing()[0]
    except:
        time.sleep(1)
        continue

    friend_game_start = 1
        

try:
    # this only plays the first active game
    gameId = client.games.get_ongoing()[0]['gameId']
    play_game(client, gameId)
except Exception as error:
    print(error)
    print("No ongoing game")