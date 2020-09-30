from authorisation import *

client = PkceAuthCode()
# print(client.get_auth())
client.open_auth()
client.refresh_access_token()
print(client.search_artist("eminem"))
print(client.search_track("Butterflies"))
