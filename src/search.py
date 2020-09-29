import authorisation

class search(authorisation.PkceAuthCode):
    """
    A class to search the api for album,artists,tracks and playlists
    """
    access_token = self.access_token

    def __init__(self, access_token):
        self.access_token = access_token

    def get_search_headers(self):
        """
        returns the header used for the get request
        """
