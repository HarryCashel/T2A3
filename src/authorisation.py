import base64
import datetime
import json
import webbrowser
from urllib.parse import urlencode
import requests
import credentials
import pkce


class PkceAuthCode(object):
    """
    A class used to grant a user access to the Spotify Api.
    Creates an access code and exchanges that code for an access token
    """
    access_token = None
    refresh_token = None
    token_is_expired = None
    access_token_expiry = datetime.datetime.now()
    authorisation_uri = "https://accounts.spotify.com/authorize"
    access_token_url = "https://accounts.spotify.com/api/token"
    search_url = "https://api.spotify.com/v1/search"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = credentials.create_client_id()
        self.client_secret = credentials.create_client_secret()
        self.code_verifier = credentials.create_code_verifier()
        self.code_challenge = pkce.get_code_challenge(self.code_verifier)

    def get_client_credentials(self):
        """
        Returns an encoded string (base64) from the client id and client secret
        :return: encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id is None or client_secret is None:
            raise Exception("""Client id and client secret are not set or out of date
                            "https://developer.spotify.com/dashboard/applications""")
        client_credentials = f"{client_id}:{client_secret}"
        client_credentials_base64 = base64.b64encode(client_credentials.encode())
        return client_credentials_base64.decode

    @staticmethod
    def get_access_token_data():
        return {
            "grant_type": "client_credentials"
        }

    def get_access_token_headers(self):
        client_credentials_base_64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_credentials_base_64}"
        }

    def get_auth_uri(self):
        authorisation_uri = self.authorisation_uri
        redirect_uri = "http://localhost:8888/callback"
        data = urlencode({"client_id": self.client_id,
                          "response_type": "code",
                          "redirect_uri": redirect_uri,
                          "code_challenge_method": "S256",
                          "code_challenge": self.code_challenge,
                          "scope": """
                          user-read-private 
                          playlist-modify-public 
                          user-library-modify 
                          user-top-read 
                          playlist-modify-private 
                          user-library-read
                          """
                          })
        lookup_url = f"{authorisation_uri}?{data}"
        return lookup_url

    def open_auth(self):
        lookup_url = self.get_auth_uri()
        webbrowser.open_new(lookup_url)

    def get_access_token_body(self):
        client_id = self.client_id
        auth_code = input("please copy the code")
        redirect_uri = "http://localhost:8888/callback"
        data = {
            "client_id": client_id,
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri,
            "code_verifier": self.code_verifier
        }
        return data

    def get_access_token(self):
        """
        A function only called in refresh_access_token.
        Used to request the initial auth token
        """
        access_token_url = self.access_token_url
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        request = requests.post(access_token_url, data=self.get_access_token_body(), headers=headers)
        access_token_response = request.json()
        valid_request = request.status_code in range(200, 299)

        if valid_request:
            now = datetime.datetime.now()
            access_token = access_token_response['access_token']
            self.access_token = access_token
            self.refresh_token = access_token_response['refresh_token']
            # access_token_type = access_token_response['token_type']
            access_token_expiry = access_token_response['expires_in']
            token_expires = now + datetime.timedelta(seconds=access_token_expiry)
            self.access_token_expiry = token_expires
            self.token_is_expired = token_expires < now  # returns True if token has expired
            return True
            # return access_token_response
        raise Exception("Could not Authenticate, please check credentials")

    def refresh_access_token(self):
        auth_success = self.get_access_token()
        if not auth_success:
            raise Exception("Authentication failed")
        token = self.access_token
        expired = self.access_token_expiry
        now = datetime.datetime.now()
        if expired < now:
            self.get_access_token()
            return self.refresh_access_token()
        return token

    def new_access_token(self):
        client_id = self.client_id
        refresh_token = self.refresh_token
        access_token_url = self.access_token_url
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id
        }
        request = requests.post(access_token_url, data=data, headers=headers)
        refresh_token_response = request.json()
        self.access_token = refresh_token_response['access_token']
        self.refresh_token = refresh_token_response['refresh_token']
        return self.access_token

    def get_search_headers(self):
        access_token = self.new_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def get_user_id(self):
        base_url = "https://api.spotify.com/v1/me"
        headers = self.get_search_headers()
        request = requests.get(base_url, headers=headers)
        response = request.text
        parsed = json.loads(response)
        return parsed['id']

    def get_search_info(self, lookup_id, resource_type="artists", version="v1"):
        base_url = "https://api.spotify.com"
        endpoint = f"{base_url}/{version}/{resource_type}/{lookup_id}"
        headers = self.get_search_headers()
        request = requests.get(endpoint, headers=headers)
        if request.status_code in range(200, 299):
            return request.json()
        raise Exception("Invalid request")

    def get_album(self, album_id):
        return self.get_search_info(album_id, resource_type="albums")

    def get_artist(self, artist_id):
        return self.get_search_info(artist_id, resource_type="artists")

    def search(self, query, search_type="artist"):
        """function that takes two strings and searches for information based on search type.
        By default the search type is artist. Valid types are album , artist, playlist, track, show and episode.
        """
        headers = self.get_search_headers()
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({"q": query, "type": search_type.lower()})
        lookup_url = f"{endpoint}?{data}"
        request = requests.get(lookup_url, headers=headers)
        if request.status_code in range(200, 299):
            data = request.text
            parsed = json.loads(data)
            return parsed
        raise Exception("Client side error")

    def get_album_id(self, query, search_type="album"):
        """A function that returns the track id of an album that we can use
        to retrieve more information from the api
        """
        self.query = query
        parsed = self.search(self.query, search_type="track")
        album_id = parsed["tracks"]["items"][0]["album"]["id"]
        return album_id

    def get_artist_id(self):
        pass

    def search_track(self, query, search_type="track"):
        """A function to search an track and return information about that track.
        Takes a string as arguement, string should be the track name
        """
        self.query = query
        parsed = self.search(self.query, search_type="track")

        artist = parsed["tracks"]["items"][0]["album"]["artists"][0]["name"]
        album = parsed["tracks"]["items"][0]["album"]["name"]
        return f"Artist: {artist}\nAlbum: {album}"

    def search_track_id(self, query, search_type="track"):
        """A function to return the uri of a song title, to use to save to a playlist we create
        """
        self.query = query
        parsed = self.search(self.query, search_type="track")
        track_uri = parsed["tracks"]["items"][0]['id']
        return track_uri

    def search_artist(self, query, search_type="artist"):
        """A function to search an artist and return information about that artist.
        Takes a string as argument, string should be the artist name
        """
        self.query = query
        parsed = self.search(self.query, search_type="artist")
        # followers = parsed["artists"]["followers"]["total"]
        followers = parsed["artists"]["items"][0]["followers"]["total"]
        genres = parsed["artists"]["items"][0]["genres"]
        return f"Followers: {followers}\nType of music: {', '.join(genres)}"

    def search_album(self, query, search_type="album"):
        """A function to search an album and return information about that album.
        Takes a string as argument, string should be the album name
        """
        self.query = query
        parsed = self.search(self.query, search_type="album")
        artist = parsed["albums"]["items"][0]["artists"][0]["name"]
        release_date = parsed["albums"]["items"][0]["release_date"]
        total_tracks = parsed["albums"]["items"][0]["total_tracks"]
        # album_uri = parsed["albums"]["items"][0]["uri"]
        return f"Artist: {artist}\nRelease Date: {release_date}\nTotal Tracks: {total_tracks}"

    def get_album_tracks(self, query):
        """Takes a string as argument and returns a list of tracks in that album
        """
        self.query = query
        album_id = self.get_album_id(query)
        headers = self.get_search_headers()
        endpoint = "https://api.spotify.com/v1/albums"
        lookup_url = f"{endpoint}/{album_id}/tracks"
        request = requests.get(lookup_url, headers=headers)
        if request.status_code in range(200, 299):
            data = request.text
            parsed = json.loads(data)
            # for i in parsed["items"]:
            #     # for j in i:
            #     #     print(j)
            #     print(i["name"])
            #     print()
            track_list = [i["name"] for i in parsed["items"]]
            return track_list

    def create_playlist(self):
        playlist_name = input("What would you like to name your playlist?\t")
        user_id = self.get_user_id()
        base_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        headers = {
            "Authorization": f"Bearer {self.new_access_token()}",
            "Content-Type": "application/json"
        }
        body = json.dumps({
            "name": f"{playlist_name}"
        })
        response = requests.post(url=base_url, data=body, headers=headers)
        if response.status_code in range(200, 299):
            return "Playlist created successfully"

    def get_playlist_id(self):
        base_url = "https://api.spotify.com/v1/me/playlists"
        headers = {
            "Authorization": f"Bearer {self.new_access_token()}"
        }
        response = requests.get(url=base_url, headers=headers)
        data = json.loads(response.text)
        names = [i['name'] for i in data['items']]
        ids = [i['id'] for i in data['items']]
        id_dictionary = dict(zip(names, ids))
        return id_dictionary

    def add_to_playlist(self):
        playlist = input("What playlist do you want to add to?\t")
        playlist_id = self.get_playlist_id()[f"{playlist}"]
        base_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        song_to_add = input("What song would you like to add?")
        song_uri = self.search_track_id(song_to_add)
        query = urlencode({"uris": f"spotify:track:{song_uri}"})
        lookup_url = f"{base_url}?{query}"
        headers = {
            "Authorization": f"Bearer {self.new_access_token()}",
            "Content-Type": "application/json"
        }

        request = requests.post(url=lookup_url, headers=headers)
        return f"{song_to_add} added to {playlist}"

    def view_playlists(self):
        base_url = f"https://api.spotify.com/v1/users/{self.get_user_id()}/playlists"
        headers = self.get_search_headers()
        request = requests.get(base_url, headers=headers)
        response = request.text
        data = json.loads(response)
        playlists = []
        for i in data['items']:
            if i['name']:
                playlists.append(i['name'])
        return playlists

    def view_playlist(self):
        playlist = input("What playlist do you want to look at?\nNote playlists are case sensitive\t")
        playlist_id = self.get_playlist_id()[f"{playlist}"]
        base_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {"Authorization": f"Bearer {self.new_access_token()}"}
        response = requests.get(url=base_url, headers=headers)
        data = json.loads(response.text)
        playlist_tracks = []
        data = data['items']
        for i in data:
            if i['track']:
                playlist_tracks.append(i['track']['name'])
        return playlist_tracks

