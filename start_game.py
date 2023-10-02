# create a game against the computer
# inputs we need: level, clock_limit, clock_increment, color
    # clock_limit needs to be a whole number of minutes in seconds (60, 120, etc.)
# unchanging inputs: days, variant, position
def create_game_ai(client):
    level = input('level (1-8):\n')
    clock_limit = input('clock limit: \n')
    clock_increment = input('clock increment: \n')
    color = input('color (black or white): \n')
    client.challenges.create_ai(level, clock_limit, clock_increment, None, color, None, None)


# create a game against a friend
# NOTE: the other player needs to accept the game before you see it on our account
# inputs we need: username, clock_limit, clock_increment, color
# unchanging inputs: rated, days, variant, position
def create_game_friend(client):
    username = input('opponent username: \n')
    clock_limit = input('clock limit: \n')
    clock_increment = input('clock increment: \n')
    color = input('color (black or white): \n')
    client.challenges.create(username, False, clock_limit, clock_increment, None, color, None, None)

    
# get_users_followed() gives an iterator of your friends
#print(next(client.relations.get_users_followed()))