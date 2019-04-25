from Helper import *
import time
import SnakeTitle
import NewGame

Players = 1
CONTINUE="continue"
Screen = None
FULL_SCREEN=None

def createMainScreen(stdscr):
    if(checkIfEnoughSpaceForGame(stdscr)):
            raise NotEnoughSpace()

    global Screen
    global FULL_SCREEN
    FULL_SCREEN=stdscr
    Screen = stdscr.subwin(MINIMUM_HEIGHT, MINIMUM_WIDTH, 0,0 )


    FULL_SCREEN.nodelay(False)  # Makes getKey blocking
    FULL_SCREEN.clear()
    FULL_SCREEN.refresh()
    Screen.box()
    Screen.refresh()

    maxY, maxX = Screen.getmaxyx()

    titleStartX = int((maxX - SnakeTitle.TITLE_WIDTH) / 2)

    SnakeTitle.SnakeTitle().main(Screen, startX=titleStartX, startY=2)

    menu = [("New Game", newGameFunc), ("Scoreboard", scoreBoardFunc), ("Exit", exitFunc)]
    maxLen= max([len(i[0]) for i in menu])

    x = int((maxX - maxLen)/2)
    y = int(maxY/2)

    createMenu(Screen, menu, startX=x, startY=y)

    Screen.refresh()
    while menu_handler(FULL_SCREEN):
        if(checkIfEnoughSpaceForGame(FULL_SCREEN)):
            raise NotEnoughSpace()

    return Players #TODO:Hauria de retornar una instancia de SnakeGame amb les snakes i config adequada

def exitFunc():
    raise ExitTotal("Thank you for playing :3")

def setUpPlayers(players):
    global Players
    Players = players
    return CONTINUE

def newGameFunc():
    result = NewGame.newGame(Screen, FULL_SCREEN)

    return CONTINUE


def scoreBoardFunc():
    pass

