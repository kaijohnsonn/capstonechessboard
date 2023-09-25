import berserk
import requests

def establish_connection():
    session = berserk.TokenSession('lip_UyYinDogVSzglgIhis7O')
    client = berserk.Client(session=session)
    response_API = requests.get('https://lichess.org')
    return client

# confirms API call
#print(client.users.get_public_data('nucapstonet4'))
#print(client.account.get())