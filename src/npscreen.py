
import authorisation
import curses
import time
from os import system, name


def clear():
    # function to clear the terminal on program exit
    # for windows os
    if name == "nt":
        _ = system("cls")
    # for mac/linux
    else:
        _ = system("clear")


def display_menu(stdscr, selected_row_id):
    # function to display main menu in the centre of terminal
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    menu = [
        "Search Artist",
        "Search Song",
        "View All Playlists",
        "Create Playlist",
        "Add Track to Playlist",
        "View Playlist",
        "Exit"
    ]

    # A loop to get coordinates for each row and highlight selected row
    for xid, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + xid

        if xid == selected_row_id:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    stdscr.addstr(1, 1, "(Use arrow keys to navigate and Enter to select)")
    stdscr.refresh()


def main(stdscr):
    # the function to call to run the program, which holds nested functions
    # and the loop that runs the program
    menu = [
        "Search Artist",
        "Search Song",
        "View All Playlists",
        "Create Playlist",
        "Add Track to Playlist",
        "View Playlist",
        "Exit"
    ]
    current_row_xid = 0
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    display_menu(stdscr, current_row_xid)

    def string_middle_screen(sentence):
        # a function that takes a string as an argument
        # and returns the x, y coordinates for the center of the curses window
        # and the string.
        h, w = stdscr.getmaxyx()
        x = w // 2 - len(sentence) // 2
        y = h // 2
        return y, x, sentence

    def curses_break():
        # function to close curses to enable certain features
        curses.nocbreak()
        stdscr.keypad(False)
        curses.noecho()
        curses.endwin()

    def display_artist():
        clear()
        curses_break()
        stdscr.clear()
        artist = client.search_artist(input("Enter an artist name:\t"))
        stdscr.addstr(f"{artist}")
        stdscr.refresh()
        stdscr.getch()
        stdscr.refresh()
        curses.wrapper(main)

    def display_track():
        clear()
        curses_break()
        stdscr.clear()
        track = client.search_track(input("Enter an song name:\t"))
        stdscr.addstr(f"{track}")
        stdscr.refresh()
        stdscr.getch()
        stdscr.refresh()
        curses.wrapper(main)

    def display_playlists():
        curses_break()
        clear()
        playlist = client.view_playlists()
        playlist = "\n".join(playlist)
        print(playlist)
        stdscr.getch()
        stdscr.refresh()
        curses.wrapper(main)

    def display_create_playlist():
        clear()
        curses_break()
        stdscr.clear()
        print(client.create_playlist())
        stdscr.refresh()
        stdscr.getch()
        stdscr.refresh()
        curses.wrapper(main)

    def display_add_to_playlist():
        clear()
        curses_break()
        stdscr.clear()
        client.add_to_playlist()
        stdscr.refresh()
        stdscr.getch()
        stdscr.refresh()
        curses.wrapper(main)

    def display_specific_playlist():
        curses_break()
        clear()
        playlist = client.view_playlist()
        playlist = "\n".join(playlist)
        print(playlist)
        stdscr.getch()
        stdscr.refresh()
        curses.wrapper(main)

    # The loop that enables the navigation and selection of features
    while 1:
        key = stdscr.getch()
        stdscr.clear()
        # conditional statement to show current highlighted option
        # and select a feature
        if key == curses.KEY_UP and current_row_xid == 0:
            current_row_xid = len(menu) - 1
        elif key == curses.KEY_UP and current_row_xid > 0:
            current_row_xid -= 1
        elif key == curses.KEY_DOWN and current_row_xid < len(menu) - 1:
            current_row_xid += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.addstr(0, 0, "You pressed {}".format(menu[current_row_xid]) + ". Press any key to continue.")
            stdscr.refresh()
            stdscr.getch()
            clear()
            # conditional statement to run selected feature
            if current_row_xid == 0:
                display_artist()
                clear()
            elif current_row_xid == 1:
                display_track()
                clear()
            elif current_row_xid == 2:
                display_playlists()
                clear()
            elif current_row_xid == 3:
                display_create_playlist()
                clear()
            elif current_row_xid == 4:
                display_add_to_playlist()
                clear()
            elif current_row_xid == 5:
                display_specific_playlist()
                clear()
            elif current_row_xid == len(menu) - 1:
                stdscr.clear()
                y, x, sentence_input = string_middle_screen("Goodbye.. =)")
                stdscr.addstr(y, x, sentence_input)
                stdscr.refresh()
                time.sleep(2)
                clear()
                quit()

        clear()
        display_menu(stdscr, current_row_xid)

        stdscr.refresh()


def welcome():
    # function to greet user on login
    name = input("Hi! Welcome to my app.\nPlease enter your name.\n")
    print(f"Alright {name}, let's get started.")
    time.sleep(2)
    clear()
    curses.wrapper(main)


def initialise():
    client.open_auth()
    client.get_access_token()
    clear()
    welcome()
    curses.wrapper(main)
    curses.endwin()
    clear()


def reset_windows():
    clear()
    curses.wrapper(main)


client = authorisation.PkceAuthCode()
initialise()
welcome()
curses.wrapper(main)
curses.endwin()
clear()
