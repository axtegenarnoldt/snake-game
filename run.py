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


WINDOW_WIDTH = 60  # number of columns of window box 
WINDOW_HEIGHT = 20  # number of rows of window box 

Score = 0


def welcome_to_snake(stdscr):
    welcome_to_snake = curses.newwin(WINDOW_HEIGHT, WINDOW_WIDTH, 0, 0)
    # Display ASCII art
    welcome_to_snake.addstr(0, 0, r"""r
         ____  _   _    _    _  _______    ____    _    __  __ _____ 
        / ___|| \ | |  / \  | |/ / ____|  / ___|  / \  |  \/  | ____|
        \___ \|  \| | / _ \ | ' /|  _|   | |  _  / _ \ | |\/| |  _|  
         ___) | |\  |/ ___ \| . \| |___  | |_| |/ ___ \| |  | | |___ 
        |____/|_| \_/_/   \_\_|\_\_____|  \____/_/   \_\_|  |_|_____| 
    """)
    welcome_to_snake.addstr(10, 0, "Press 'p' to play game or 'r' to view rules")
    welcome_to_snake.refresh()

def display_rules(stdscr):
    rules_window = curses.newwin(WINDOW_HEIGHT, WINDOW_WIDTH, 0, 0)
    rules_window.addstr("Rules of the game:")
    rules_window.addstr("1. Move the snake by pressing the arrow keys.")
    rules_window.addstr("2. Eat the food to increase your score.")
    rules_window.addstr("3. The game ends if you hit the border or the snake.") 
    rules_window.addstr("4. Press 'q' if you want to end game.")
    rules_window.addstr("5. Press any key to go back to menu.")
    rules_window.refresh()
    rules_window.getch()

def start_area(stdscr):
    while True:
        welcome_to_snake(stdscr)
        user_input = stdscr.getch()
        if user_input == ord('p'):
            break
        elif user_input == ord('r'):
            stdscr.clear()
            display_rules(stdscr)

def main_game(stdscr):
    # playground
    curses.initscr()
    curses.start_color()
    game_area = curses.newwin(WINDOW_HEIGHT, WINDOW_WIDTH, 0, 0)
    game_area.keypad(1)
    game_area.border()
    game_area.nodelay(1)
    game_area.timeout(100)
    
    #color for the snake
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    # Colors for the food
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    Score = 0

    # snake and food
    snake = [(5, 4), (4, 3), (4, 2)]
    food = (8, 8)

    game_area.addch(food[0], food[1], '#')

    # Inital direction of the snake
    direction = 'RIGHT'

    
    while True:
        game_area.addstr(0, 2, 'Score ' + str(Score) + '')
        game_area.refresh()
        time.sleep(0.1)
        game_area.timeout(150 - (len(snake)) // 5 + len(snake)//10 % 120) # increase speed
        

        #Handel user input
        event = game_area.getch()
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

        if snake[0] == food:
            Score += 1
            food = ()
            while food == ():
                food = (random.randint(1, WINDOW_HEIGHT - 2), random.randint(1, WINDOW_WIDTH - 2)) # Generate new food
                if food in snake:
                    food = ()
            food_color_pair = random.choice([2, 3, 4, 5, 6])
            game_area.addch(food[0], food[1], '#', curses.color_pair(food_color_pair))
        else: 
            last = snake.pop()
            game_area.addch(last[0], last[1], ' ')

    
     
            game_area.addch(snake[0][0], snake[0][1], '@', curses.color_pair(1))

    # End curses
    curses.endwin()
    
if __name__ == "__main__":
    curses.wrapper(welcome_to_snake)
    curses.wrapper(start_area)
    curses.wrapper(main_game)
   
