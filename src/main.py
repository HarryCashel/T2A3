from npscreen import *

print("Welcome to the Spotify App!")
print("All the functionality of Spotify except you can't listen to music...yet!")
print("If you're running this I will assume you have linked your Spotify account to a Spotify Developer account")
print("Have your client id and client secret and we'll get started.")

initialise()
welcome()
curses.wrapper(main)
curses.endwin()
clear()
