import curses
from curses import wrapper
import time
import random



def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr('welcome to the speed type tester')
    stdscr.addstr('\nPress any key to begin!')
    stdscr.refresh()
    stdscr.getkey()

def display_txt(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1,0, f'WPM {wpm}')


    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)


        stdscr.addstr(0, i, char, color)


def load_text():
    with open('text.txt', 'r') as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def wpm_test(stdscr):
    target_txt = load_text()
    current_txt = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed =max(time.time() - start_time, 1)
        wpm = round((len(current_txt) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_txt(stdscr, target_txt, current_txt, wpm)
        stdscr.refresh() 

        if ''.join(current_txt) == target_txt:
            stdscr.nodelay(False)
            break
        
        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break   
        if key in ('KEY_BACKSPACE', '\b', '\x7f'):
            if len(current_txt)>0:
                current_txt.pop()
        elif len(current_txt) < len(target_txt):
            current_txt.append(key)



def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    start_screen(stdscr)

    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, 'You completed the text! press any key to continue')
        key = stdscr.getkey()
        
        if ord(key) == 27:
            break


wrapper(main)    