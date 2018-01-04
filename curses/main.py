import curses
from curses import wrapper

def firstSetup(stdscr):
    stdscr.clear()
    three_col_w = int(curses.COLS/3)
    win1= curses.newwin(curses.LINES,three_col_w,0,0)
    win2 = curses.newwin(curses.LINES,three_col_w,0,three_col_w)
    win3 = curses.newwin(curses.LINES,three_col_w,0,three_col_w*2)
    win1.border(0)
    win2.border(0)
    win3.border(0)
    stdscr.addstr(0,1,"Welcome to DashTerm")

    stdscr.refresh()
    win1.refresh()
    win2.refresh()
    win3.refresh()
    x = stdscr.getch()

def main(stdscr):
    firstSetup(stdscr)

wrapper(main)
