from settings import but1_pressed, but2_pressed
from lcds import *
import time

# create a game against the computer
# inputs we need: level, clock_limit, clock_increment, color
    # clock_limit needs to be a whole number of minutes in seconds (60, 120, etc.)
# unchanging inputs: days, variant, position
def create_game_ai(client):
    level = scroll_options("Level", {1,2,3,4,5,6,7,8})
    color = scroll_options("Color", {"black", "white"})
    timed = scroll_options("Timed", {"yes", "no"})
    if timed == 'yes':
        clock_limit = scroll_options("Clock Limit", {60, 120})
        clock_increment = scroll_options("Clock Inc.", {3})
        client.challenges.create_ai(level, clock_limit, clock_increment, None, color, None, None)
    else:
        client.challenges.create_ai(level = level, color = color)
        clear_lcd1()
        clear_lcd2()
    return color


# create a game against a friend
# NOTE: the other player needs to accept the game before you see it on our account
# inputs we need: username, clock_limit, clock_increment, color
# unchanging inputs: rated, days, variant, position
def create_game_friend(client):
    username = get_friends(client)
    color = scroll_options("Color", {"black", "white"})
    timed = scroll_options("Timed", {"yes", "no"})
    if timed == 'yes':
        clock_limit = scroll_options("Clock Limit", {60, 120})
        clock_increment = scroll_options("Clock Inc.", {3})
        client.challenges.create(username, False, clock_limit, clock_increment, None, color, None, None) 
    else:
        client.challenges.create(username = username, color = color, rated = False)        
        clear_lcd1()
        clear_lcd2()
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

    return scroll_options("User", dict.values())

def scroll_options(option_name, options):
    i = 0
    clear_lcd1()
    clear_lcd2()
    print_lcd1(option_name + ": " + str(list(options)[i]))
    print_lcd2("Select")
    
    while True:
        # Check if buttons are pressed
        if but1_pressed[0]:
            i+=1
            if i >= len(options):
                i = 0
            but1_pressed[0] = False  # Reset the flag
            clear_lcd1()
            print_lcd1(option_name + ": " + str(list(options)[i]))

        if but2_pressed[0]:
            but2_pressed[0] = False  # Reset the flag
            print(option_name + ": " + str(list(options)[i]) + " selected")
            return list(options)[i]

        time.sleep(0.1)
