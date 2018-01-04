import curses
from curses import wrapper

def main(stdscr):
    stdscr.clear()
    half_y = int(curses.COLS / 2)
    win  = curses.newwin((curses.LINES ),(half_y),0,half_y)
    win_2 = curses.newwin((curses.LINES ),(half_y ),0,0)
    win.border(0)
    win_2.border(0)
    win.addstr(0,1,"This is the title")

    for i in range(2,11):
        win.addstr(i,3,"Example "+str(i-2))

    stdscr.refresh()
    win.refresh()
    win_2.refresh()
    x = stdscr.getch()

wrapper(main)
