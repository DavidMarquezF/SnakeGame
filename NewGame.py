import curses
from Helper import *
from curses.textpad import Textbox, rectangle

Screen=None
tabScreen=None
CurrentSelectedTab = 0
FULL_SCREEN=None

def newGame(screen, stdsrc):
    global Screen
    global tabScreen
    global CurrentSelectedTab
    global FULL_SCREEN

    FULL_SCREEN = stdsrc
    Screen = screen

    CurrentSelectedTab = 0

    Screen.erase()
    Screen.box()

    newGameOpts = NewGameOpts()

    Screen.hline(2, 1, curses.ACS_HLINE, MINIMUM_WIDTH - 2)

    tabScreen = Screen.subwin(MINIMUM_HEIGHT-5, MINIMUM_WIDTH - 2, 3, 1)
    tabScreen.box()

    Screen.refresh()

    while True:
        drawTabs(CurrentSelectedTab, newGameOpts)




def handleKeys():
    global CurrentSelectedTab
    
    key = FULL_SCREEN.getch()
    if key == curses.KEY_LEFT:
        if CurrentSelectedTab == 0:
            raise GoBackToMainScreen()
        CurrentSelectedTab -= 1
    elif key == curses.KEY_RIGHT:
        if CurrentSelectedTab == 1:
            raise FinishedGamePrep()
        CurrentSelectedTab += 1

    return key

def drawTabs(CurrentSelectedTab, newGameOpts):
    if(CurrentSelectedTab == 0):
        backText = "<- Exit"
        nextText = " Next ->"
    else:
        backText="<- Back"
        nextText = "Start ->"


    Screen.addstr(MINIMUM_HEIGHT - 2, 2, backText)
    Screen.addstr(MINIMUM_HEIGHT - 2, MINIMUM_WIDTH - len(nextText) - 2, nextText)
    Screen.addstr(1, 1, "Players", curses.A_STANDOUT if CurrentSelectedTab == 0 else curses.A_NORMAL)
    Screen.addstr(1, 9, "|")
    Screen.addstr(1, 11, "Options", curses.A_STANDOUT if CurrentSelectedTab == 1 else curses.A_NORMAL)
    Screen.refresh()

    tabPlayers(newGameOpts) if CurrentSelectedTab == 0 else tabOptions(newGameOpts)


def tabPlayers(newGameOpts):
    tabScreen.clear()
    tabScreen.addstr(1,1, "P", hotkey_attr)
    tabScreen.addstr(1,2, "layers: {}".format(len(newGameOpts.players)), menu_attr)
    tabScreen.refresh()

    key = handleKeys()
    if key in (ord("p"), ord("P")):
        s = curses.newwin(6, 13, 3, 11)
        s.box()
        s.addstr(1, 2, "1", hotkey_attr)
        s.addstr(1, 3, " Player", menu_attr)
        s.addstr(2, 2, "2", hotkey_attr)
        s.addstr(2, 3, " Players", menu_attr)
        s.addstr(3, 2, "3", hotkey_attr)
        s.addstr(3, 3, " Players", menu_attr)
        s.addstr(4, 2, "4", hotkey_attr)
        s.addstr(4, 3, " Players", menu_attr)
        s.refresh()

        key_players = s.getch()
        if(key_players in (ord("1"), ord("2"), ord("3"), ord("4"))):
            newGameOpts.players = ["P"+str(i+1) for i in range(int(chr(key_players)))]
        s.erase()
        s.refresh()
    createEditBox(10,5).edit()


    #box.edit()

    #box.gather()
    return
    curses.echo()
    maxLetters=8
    x1 = 10
    y1 = 5
    tabScreen.addstr(y1, x1, " " * maxLetters, curses.A_UNDERLINE)
    newGameOpts.players[0] = tabScreen.getstr(y1, x1, maxLetters)
    curses.noecho()

def createEditBox(startX, startY, maxLen = 10):
    editWin = tabScreen.subwin(1, maxLen, startY + 1, startX + 1)
    rectangle(tabScreen, startY, startX, 1 + startY, maxLen + startX + 1) #rectangle(screen, y de cantonada esquerra de dalt, x de c. e. de dalt, y de c. dreta baix

    tabScreen.refresh()
    box = Textbox(editWin, )
    return box

def tabOptions(newGameOpts):
    tabScreen.clear()
    tabScreen.refresh()

    key = handleKeys()


def playerTab():
    pass


class NewGameOpts(object):
    def __init__(self):
        self.players = ["P1"]

class FinishedGamePrep(Exception):
    pass