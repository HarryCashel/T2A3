from authorisation import *
import requests
import json
from urllib.parse import urlencode


class Search(PkceAuthCode):
    """
    A class to search the api for album,artists,tracks and playlists
    """
    search_url = "https://api.spotify.com/v1/search"
    # client_id = client_id
    search_access_token = PkceAuthCode().new_access_token()

    def __init(self, *args, client_id, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id

    def basic_search(self, query, search_type="artist"):
        """function that takes two strings and searches for information based on search type.
        By default the search type is artist. Valid types are album , artist, playlist, track, show and episode.
        returns json data we use in later search functions.
        """
        headers = {
            "Authorization": f"Bearer {self.search_access_token}"
        }
        endpoint = self.search_url
        data = urlencode({"q": query, "type": search_type.lower()})
        lookup_url = f"{endpoint}?{data}"
        request = requests.get(lookup_url, headers=headers)
        return self.search_access_token
        if request.status_code in range(200, 299):
            data = request.json()
            parsed = json.load(data)
            return parsed
        return request.status_code

    def search_artist(self):
        """
        Uses the basic_search function to search the api for artist names, stores the artist ID for later use
        and returns information on the artist.
        """
        pass


