import curses
import os
from utils import run_command, load_config, apply_custom_colors, handle_keys

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.json')

    try:
        config = load_config(config_path)
    except Exception as e:
        stdscr.addstr(0, 0, str(e))
        stdscr.refresh()
        stdscr.getch()
        return

    apply_custom_colors(stdscr)

    items = config.get('items', [])
    if not items:
        stdscr.addstr(0, 0, "No items found in configuration.")
        stdscr.refresh()
        stdscr.getch()
        return

    current_row = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        for idx, item in enumerate(items):
            x = w // 2 - len(item['title']) // 2
            y = h // 2 - len(items) // 2 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))  
                stdscr.addstr(y, x, item['title'])
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, item['title'], curses.color_pair(2))  

        stdscr.refresh()

        key = stdscr.getch()
        result, current_row = handle_keys(stdscr, key, items, current_row)
        if result == 'quit':
            break
        elif result:
            stdscr.clear()
            stdscr.refresh()
            return result

if __name__ == "__main__":
    command = curses.wrapper(main)
    if command:
        run_command(command)
