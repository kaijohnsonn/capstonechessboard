# create a game against the computer
# inputs we need: level, clock_limit, clock_increment, color
    # clock_limit needs to be a whole number of minutes in seconds (60, 120, etc.)
# unchanging inputs: days, variant, position
def create_game_ai(client):
    level = input('level (1-8):\n')
    color = input('color (black or white): \n')
    timed = input('timed (y or n):\n')
    if timed == 'y':
        clock_limit = input('clock limit: \n')
        clock_increment = input('clock increment: \n')
        client.challenges.create_ai(level, clock_limit, clock_increment, None, color, None, None)
    else:
        client.challenges.create_ai(level = level, color = color)
    return color


# create a game against a friend
# NOTE: the other player needs to accept the game before you see it on our account
# inputs we need: username, clock_limit, clock_increment, color
# unchanging inputs: rated, days, variant, position
def create_game_friend(client):
    username = get_friends(client)
    color = input('color (black or white): \n')
    timed = input('timed (y or n):\n')
    if timed == 'y':
        clock_limit = input('clock limit: \n')
        clock_increment = input('clock increment: \n')
        client.challenges.create(username, False, clock_limit, clock_increment, None, color, None, None)
    else:
        client.challenges.create(username = username, color = color, rated = False)
    return color


def get_friends(client):
    dict = {} 
    counter = 1
    iterable = client.relations.get_users_followed()

    # list friends
    for item in iterable:
        dict[counter] = item['id']
        print(str(counter) + " " + item['id']) 
        counter += 1

    user = input('opponent username number: \n')
    return dict[int(user)]