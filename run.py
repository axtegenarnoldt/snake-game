import random
import time
import gspread
import os
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

#structur for the playground and how to create snake and food
#are taken from Patrick Loebers youtube: https://www.youtube.com/watch?v=M_npdRYD4K0

WINDOW_WIDTH = 60  # number of columns of window box 
WINDOW_HEIGHT = 20 # number of rows of window box 

# playground
def main_game(win):
    curses.initscr()
    game_area = curses.newwin(WINDOW_HEIGHT, WINDOW_WIDTH, 0, 0)
    game_area.keypad(1)
    game_area.nodelay(1)
    game_area.timeout(100)

    Score = 0

    # snake and food
    snake = [(5, 4), (4, 3), (4, 2)]
    food = (8, 8)

    win.addch(food[0], food[1], '#')

    # Inital direction of the snake
    direction = 'RIGHT'

    
    while True:
        win.addstr(0, 2, 'Score ' + str(Score) + '')
        win.refresh()
        time.sleep(0.2)

        #Handel user input
        event = win.getch()
        if event == ord('q'):
            break
        elif event == curses.KEY_UP:
            direction = 'UP'
        elif event == curses.KEY_DOWN:
            direction = 'DOWN'
        elif event == curses.KEY_LEFT:
            direction = 'LEFT'
        elif event == curses.KEY_RIGHT:
            direction = 'RIGHT'

        # Directions to move the snake
        y = snake[0][0]
        x = snake[0][1]
        if direction == 'DOWN':
            y += 1
        if direction == 'UP':
            y -= 1
        if direction == 'LEFT':
            x -= 1
        if direction == 'RIGHT':
            x += 1

        snake.insert(0, (y, x))

        # If the snake runs in to border or itself game ends
        if y < 0 or y >= 25 or x < 0 or x >= 60:
            break # border
        if (y, x) in snake[1:]:
            break # itself

        if (y, x) == food:
            Score += 1
            win.addch(food[0], food[1], ' ')
            food = (random.randint(1, WINDOW_HEIGHT - 2), random.randint(1, WINDOW_WIDTH - 2)) # Generate new food
        else:
            last = snake.pop()
            win.addch(last[0], last[1], ' ')
    
     
        win.addch(snake[0][0], snake[0][1], '*')

    # End curses
    curses.endwin()

if __name__ == "__main__":
 curses.wrapper(main_game)
