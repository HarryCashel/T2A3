#Spotify CLI Application

##Description

This app uses SpotifyforDevelopers to allow a user to search for artists, songs and albums. 
The user can create, view and edit playlists.

To use this app you will need to link your Spotify account with a Spotify Developer account.

Create a Spotify Developer account here https://developer.spotify.com/  
You will be required to enter the client_id and client_secret into the terminal.


##Solution

The application is broken into a class to authenticate the user, retrieve data
and send data back and other functions to take the user input, display confirmation
and allow navigation of the application.

* API requests are handled using the requests library.
* Parsing the data is done with the json library.
* To encode strings and format strings the urlencode, base64 and pkce libraries were used.
* Time and datetime library is used to keep track of the remaining time of an access token
and whether it needs to be refreshed.
* To display data and take user input the curses library was sufficient. I'd like to come
back and use the npyscreen library as I think it offers more flexibility and presents data
in a more digestible format.

Before we connect to the API we need to do some housekeeping. We need to encode the
client credentials, construct the authorisation uri, and set the necessary scopes 
(the permissions the user must grant the app in order to perform it's functions ).
These are done in the functions:
* get_client_credentials()
* get_auth_uri()


The initial authorisation request to the Spotify API requires:
* A client ID number
* A client secret 
* A redirect URI
* Authorisation Code

Using the first three pieces of data, the function open_auth() opens a webbrowser with the 
webbrowser library. This is were the user grabs the authorisation code (Currently 
the user must manually past the code from the url, in the future a http server will facilitate
the automation of this step).

Using these three pieces of data and our authorisation code , the function get_access_token() sends a POST request
to a Spotify Web API endpoint to exchange for an access token that is used to request
and send data to and from the API. Refreshing the access token is handled using the functions
new_access_token() and refresh_access_token().

The overview HTTP functionality of the application is as follows:
* POST request for access token
* POST request to refresh token
* GET request for all search functions
* POST request to create playlist
* POST request to add songs to a playlist 


##Installation
#### Dependencies
*base64  
*datetime  
*json  
*urlencode  
*requests  
*pkce
*curses


###Set up
Create a Spotify Developer account here https://developer.spotify.com/
Keep your client id and client secret ready

From you environment

  `pip install -r requirements.txt`
  
From the root directory 

  `python src/main.py`

You will be asked to copy the code from the url of the webpage that pops up.
Just copy and paste it into the terminal as you did for your client credentials.

Navigate the menu with arrow keys and confirm with the return key.
