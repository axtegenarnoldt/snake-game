import random
import time
import gspread
import curses
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("snake_highscore")

# structur for the playground and how to create snake and food
# are taken from Patrick Loebers youtube: https://www.youtube.com/watch?v=M_npdRYD4K0

# playground
curses.initscr()
win = curses.newwin(20, 60, 0, 0,)
win.keypad(1)
curses.noecho()
curses.curs_set(0) # hide cursor
win.border(0) # draws border
win.nodelay(True)

snake = [(4, 4), (4, 3), (4, 2)]
food = (6, 6)

win.addch(food[0], food[1], '#')
win.addch(snake[0][0], snake[0][1], '=')

while True:
    event = win.getch()
    if event == ('s'):
     event = win.getch()
     if event == ('q'):
        break
    elif event == curses.KEY_UP:
        direction = 'UP'
    elif event == curses.KEY_DOWN:
        direction = 'DOWN'
    elif event == curses.KEY_LEFT:
        direction = 'LEFT'
    elif event == curses.KEY_RIGHT:
        direction = 'RIGHT'



      
