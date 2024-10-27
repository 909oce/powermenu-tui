import json
import curses
import subprocess

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e}")

def load_config(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def apply_custom_colors(stdscr):
    curses.start_color()
    curses.use_default_colors()  

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, -1)

def handle_keys(stdscr, key, items, current_row):
    if key == curses.KEY_UP:
        current_row = (current_row - 1) % len(items)
    elif key == curses.KEY_DOWN:
        current_row = (current_row + 1) % len(items)
    elif key == ord('q') or key == ord('Q'):
        return 'quit', current_row
    elif key == curses.KEY_ENTER or key in [10, 13, ord(' ')]:
        selected_item = items[current_row]
        return selected_item['command'], current_row
    return None, current_row

