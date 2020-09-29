import requests
import json
import base64
import datetime
from time import sleep
import urllib
from urllib.parse import urlencode
import pkce
import urllib.request
import webbrowser
from credentials import *


class PkceAuthCode(object):
    """
    A class used to grant a user access to the Spotify Api.
    Creates an access code and exchanges that code for an access token
    """
    access_token = None
    refresh_token = None
    client_id = client_id
    client_secret = client_secret
    token_is_expired = None
    access_token_expiry = datetime.datetime.now()
    authorisation_uri = "https://accounts.spotify.com/authorize"
    access_token_url = "https://accounts.spotify.com/api/token"

    def __init(self, *args, client_id, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id

    def get_client_credentials(self):
        """
        Returns an encoded string (base64) from the client id and client secret
        :return: encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        print(client_id)
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
        data = urlencode({"client_id": client_id,
                          "response_type": "code",
                          "redirect_uri": redirect_uri,
                          "code_challenge_method": "S256",
                          "code_challenge": code_challenge,
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

    # def get_auth(self):
    #     access_token_url = self.access_token_url
    #     access_token_data = self.get_access_token_data()
    #     access_token_headers = self.get_access_token_headers()
    #     request = requests.post(access_token_url, data=access_token_data, headers=access_token_headers)
    #     # print(request.json())
    #     valid_request = request.status_code in range(200, 299)
    #     return request.status_code
    #     # access_token_response = request.json()
    #
    #     if valid_request:
    #         now = datetime.datetime.now()
    #         access_token = access_token_response['access_token']
    #         self.access_token = access_token
    #         access_token_type = access_token_response['token_type']
    #         access_token_expiry = access_token_response['expires_in']
    #         token_expires = now + datetime.timedelta(seconds=access_token_expiry)
    #         self.access_token_expiry = token_expires
    #         self.token_is_expired = token_expires < now  # returns True if token has expired
    #         return True
    # raise Exception("Could not Authenticate, please check credentials")

    # @staticmethod
    # def access_token_headers():
    #     return {
    #         "Content-Type": "application/x-www-form-urlencoded"
    #     }

    def get_access_token_body(self):
        client_id = self.client_id
        auth_code = input("please copy the code")
        redirect_uri = "http://localhost:8888/callback"
        data = {
            "client_id": client_id,
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri,
            "code_verifier": code_verifier
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
        valid_request = request.status_code in range(200,299)

        if valid_request:
            now = datetime.datetime.now()
            access_token = access_token_response['access_token']
            self.access_token = access_token
            self.refresh_token = access_token_response['refresh_token']
            access_token_type = access_token_response['token_type']
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


client = PkceAuthCode()
# print(client.get_auth())
client.open_auth()
# print(client.get_access_token_body())
# print(client.get_access_token())
print(client.refresh_access_token())
print(client.new_access_token())
print(client.new_access_token())