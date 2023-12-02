import time
from settings import but1_pressed, but2_pressed
from start_game import *
from LIChessAPI import *
from moves import *
from lcds import *
from buttons import *

client = establish_connection()

print_lcd1("Play Friend")
print_lcd2("Play Computer")
friend_game_start = 1

while True:
    # Check if buttons are pressed
    if but1_pressed[0]:
        but1_pressed[0] = False  # Reset the flag
        color = create_game_friend(client)
        friend_game_start = 0
        break

    if but2_pressed[0]:
        but2_pressed[0] = False  # Reset the flag
        color = create_game_ai(client)
        break

    time.sleep(0.1)


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
    print_lcd1("No ongoing game")
