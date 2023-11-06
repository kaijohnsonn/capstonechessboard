import time
from start_game import *
from LIChessAPI import *
from moves import *


client = establish_connection()

color = create_game_ai(client)
#color = create_game_friend(client)

friend_game_start = 0
# allows time for the friend to accept the game
while friend_game_start == 0:
    try:
        client.games.get_ongoing()[0]
    except:
        time.sleep(1)
        continue

    friend_game_start = 1
        

try:
    # plays the first active game
    gameId = client.games.get_ongoing()[0]['gameId']
    stream_game_state(client, gameId, color)
except Exception as error:
    print(error)
    print("No ongoing game")