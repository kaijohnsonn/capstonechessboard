from start_game import *
from LIChessAPI import *

# TODO: 
# Determine how we want to organize the program
# Get inputs to start the game from the board
# Get a list of friends to choose from to start the game against

client = establish_connection()

create_game_ai(client)
#create_game_friend(client)