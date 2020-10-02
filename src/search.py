
# !/usr/sbin/python

import curses
import time
import calendar
import pytz
from datetime import datetime, timezone
from tzlocal import get_localzone
from os import system, name
import sys
import os


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
    menu = ["Calendar", "Calculator", "Clock", "Close"]

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
    menu = ["Calendar", "Calculator", "Clock", "Close"]
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

    def display_calendar(stdscr):
        today = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year

        stdscr.clear()
        stdscr.addstr(2, 2, calendar.month(year, month, 2, 1))
        stdscr.refresh()
        print("\n\nPress any key to return to main menu.\n\n")
        stdscr.getch()
        stdscr.refresh()
        curses.wrapper(main)

    def calculator():
        # a function that runs the calculator feature
        curses_break()
        clear()

        print("""The valid operators are: "+" "-" "/" "*" """)
        calc = input("Type calculation:\n")
        try:
            print("Answer: " + str(eval(calc)))
            calculate_again()
        except:
            print("""
            Enter a valid operation in the format
            a * b, a + b, a - b or a / b, where a and b are integers. 
            """)
            calculate_again()

    def calculate_again():
        # function to offer user to run calculator function again
        calc_again = input("""
        Do you want to run calculator again?
        Press any key to continue or N to return to main menu
        """)
        if calc_again.lower() == "y":
            calculator()
        elif calc_again.lower() == "n":
            clear()
            curses.wrapper(main)
        else:
            calculator()

    def clock():
        # function to run the clock feature
        curses_break()

        nsw_time = pytz.timezone("Australia/NSW")
        act_time = pytz.timezone("Australia/ACT")
        lhi_time = pytz.timezone("Australia/LHI")
        wa_time = pytz.timezone("Australia/Perth")
        tas_time = pytz.timezone("Australia/Tasmania")
        sa_time = pytz.timezone("Australia/Adelaide")
        nt_time = pytz.timezone("Australia/North")

        date_times = {
            "nsw": datetime.now(nsw_time).strftime("%H:%M:%S"),
            "qld": datetime.now(nsw_time).strftime("%H:%M:%S"),
            "act": datetime.now(act_time).strftime("%H:%M:%S"),
            "lhi": datetime.now(lhi_time).strftime("%H:%M:%S"),
            "wa": datetime.now(wa_time).strftime("%H:%M:%S"),
            "tas": datetime.now(tas_time).strftime("%H:%M:%S"),
            "sa": datetime.now(sa_time).strftime("%H:%M:%S"),
            "nt": datetime.now(nt_time).strftime("%H:%M:%S")
        }

        location = input("\nWhat Aus state are you in?\n\n")

        if location.lower() == "qld" or location.lower() == "queensland":
            print("\nlocal time: {}".format(date_times["nsw"]))
        elif location.lower() == "nsw" or location.lower() == "new south wales":
            print("\nlocal time: {}".format(date_times["nsw"]))
        elif location.lower() == "sa" or location.lower() == "south australia":
            print("\nlocal time: {}".format(date_times["sa"]))
        elif location.lower() == "tas" or location.lower() == "tasmania":
            print("\nlocal time: {}".format(date_times["tas"]))
        elif location.lower() == "act" or location.lower() == "australian capital territory":
            print("\nlocal time: {}".format(date_times["act"]))
        elif location.lower() == "nt" or location.lower() == "northern territory":
            print("\nlocal time: {}".format(date_times["nt"]))
        elif location.lower() == "wa" or location.lower() == "western australia":
            print("\nlocal time: {}".format(date_times["wa"]))
        else:
            print("""
                Enter a valid Australian state in the format
                nsw, tas, nt, wa, nt, qld, sa, act. 
                """)
            time.sleep(1)
            run_clock_again()

        # time.sleep(2)
        run_clock_again()

    def run_clock_again():
        # function to offer user to re-run the clock feature
        clock_again = input("""
        Do you want to run clock again?
        Press any key to continue or N to return to main menu
        """)
        if clock_again.lower() == "y":
            clock()
        elif clock_again.lower() == "n":
            clear()
            curses.wrapper(main)
        else:
            clock()

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

            # conditional statement to run selected feature
            if current_row_xid == 0:
                stdscr.clear()
                # y, x, sentence_input = string_middle_screen(calendar.month(year, month, 2, 1))
                # stdscr.addstr(y, x, sentence_input)
                stdscr.refresh()
                display_calendar(stdscr)
            elif current_row_xid == 1:
                calculator()

            elif current_row_xid == 2:
                clock()

            elif current_row_xid == len(menu) - 1:
                stdscr.clear()
                y, x, sentence_input = string_middle_screen("Goodbye.. =)")
                stdscr.addstr(y, x, sentence_input)
                stdscr.refresh()
                time.sleep(2)
                # sys.exit(1)
                quit()

        display_menu(stdscr, current_row_xid)

        stdscr.refresh()

    stdscr.refresh()


def welcome():
    # function to greet user on login
    name = input("Hi! Welcome to my app.\nPlease enter your name.\n")
    print(f"Alright {name}, let's get started.")
    time.sleep(2)
    curses.wrapper(main)


if len(sys.argv) > 2:
    print("\n Please use --help to see flag options")
else:
    if "--help" in sys.argv:
        print("\n--navigation")
        print("Will show you how to navigate the application")

        print("\n--future")
        print("Will show the user planned future updates\n")

    elif "--navigation" in sys.argv:
        print("From the main menu you can use the arrow keys to select a feature and run it with Enter")
    elif "--future" in sys.argv:
        print(
            "In the future I will add a weather feature that will take your location and give you a day/5day/week forecast with features like temp, feelslike, and whether rain is expected")
    else:
        welcome()
        curses.wrapper(main)
        curses.endwin()
        clear()


