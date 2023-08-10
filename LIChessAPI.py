import berserk
import requests

session = berserk.TokenSession('lip_JMyZWpXAFOfLefFVXf4Z')
client = berserk.Client(session=session)
response_API = requests.get('https://lichess.org')
# confirms API call
# print(client.users.get_public_data('nucapstonet4'))
print(client.account.get())

