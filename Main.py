"""
Recordar, molt important: Fer anar aixo amb python 3. Aixo vol dir que a la terminal s'ha d'entrar python3 Main.py


"""
from curses import wrapper
from Controller import  Controller
from SnakeGame import *

from Helper import *
import PantallaPrincipal

def printScreen(screenRepr):
    """
    Printeja la screen. Peta si no pot fer cabre totes les lnies
    :param screenRepr:
    :return:
    """
    for y, line in enumerate(screenRepr):
        for x, char in enumerate(line):
            if("part" in char):
                MAP_SCREEN.addstr(y + 1, x + 1, " ", curses.color_pair(10))#White body
            elif("head" in char):
                MAP_SCREEN.addstr(y + 1, x + 1, " ", curses.color_pair(int(char[4:])))
            else:
                MAP_SCREEN.addstr(y + 1, x + 1, char)
    MAP_SCREEN.refresh()

def printStats(stats):

    maxLen = 0
    for key in stats.keys():
        if len(key) > maxLen:
            maxLen = len(key)
    foodX = 1 + maxLen + 1
    killX = 4 + maxLen + 1
    deathX = 7 + maxLen + 1
    livesX = 10 + maxLen + 1
    timeX = 13 + maxLen + 1
    respawnX = 18 + maxLen + 1

    STATS_SCREEN.addstr(1, foodX, "F")
    STATS_SCREEN.addstr(1, killX, "K")
    STATS_SCREEN.addstr(1, livesX, "L")
    STATS_SCREEN.addstr(1, deathX, "D")
    STATS_SCREEN.addstr(1, timeX, "T")
    STATS_SCREEN.addstr(1, respawnX, "R")

    for y, key in enumerate(stats.keys()):
        STATS_SCREEN.addstr(y + 2, 1, key, curses.color_pair(y + 1))
        STATS_SCREEN.addstr(y + 2, foodX, str(stats[key].foodEaten))
        STATS_SCREEN.addstr(y + 2, killX, str(stats[key].snakesKilled))
        STATS_SCREEN.addstr(y + 2, deathX, str(stats[key].deaths))
        STATS_SCREEN.addstr(y + 2, livesX, str(stats[key].lives))
        timeAlive = str(stats[key].getTimeAlive())
        STATS_SCREEN.addstr(y + 2, timeX, timeAlive + " " * (respawnX - timeX - len(timeAlive)))
        respwanTime=str(stats[key].getCountDown())
        STATS_SCREEN.addstr(y + 2, respawnX, respwanTime + " " * (3 - len(respwanTime)))


    STATS_SCREEN.refresh()

FULL_SCREEN = None

GAME_SCREEN = None
MAP_SCREEN = None
STATS_SCREEN = None

PAUSED = False

def main(stdscr):
    global FULL_SCREEN
    FULL_SCREEN = stdscr

    setCursesLogic()


    while True:
        try:
            snakeGame = PantallaPrincipal.createMainScreen(FULL_SCREEN)



            snakeGame = SnakeGame()
            snakeGame.addSnake("P1")
            snakeGame.addSnake("Irene Mollet")
            # screen.addSnake("P3")

            FULL_SCREEN.nodelay(True)  # Makes getKey non-blocking
            FULL_SCREEN.clear()
            while True:
                try:
                    global MAP_SCREEN
                    global STATS_SCREEN
                    global GAME_SCREEN
                    global PAUSED

                    if(checkIfEnoughSpaceForGame(FULL_SCREEN, snakeGame)):
                        raise NotEnoughSpace("Current max: {0}, Needed space: {1}".format(
                            "x: {0} y: {1}".format(FULL_SCREEN.getmaxyx()[1], FULL_SCREEN.getmaxyx()[0]),
                            "x: {0} y: {1}".format(snakeGame.sizeX, snakeGame.sizeY)))
                    GAME_SCREEN = FULL_SCREEN.subwin(snakeGame.sizeY + 2 + heightStatScreen, snakeGame.sizeX+2+1,0,0)
                    MAP_SCREEN = GAME_SCREEN.subwin(snakeGame.sizeY + 2, snakeGame.sizeX + 2, 0, 0)
                    MAP_SCREEN.box()

                    STATS_SCREEN = FULL_SCREEN.subwin(heightStatScreen, snakeGame.sizeX + 2, snakeGame.sizeY + 2, 0)
                    STATS_SCREEN.box()

                    handleGame(snakeGame)

                except NotEnoughSpace as err:
                    PAUSED = True
                    notEnoughSpaceScreen(FULL_SCREEN, snakeGame)
                    PAUSED = False
                except GoBackToMainScreen:
                    Snake.PlayerNum = 1
                    break
        except NotEnoughSpace:
            notEnoughSpaceScreen(FULL_SCREEN)
        except GoBackToMainScreen:
            pass



def notEnoughSpaceScreen(stdscr, snakeGame = None):
    stdscr.erase()
    stdscr.box()
    stdscr.refresh()
    while checkIfEnoughSpaceForGame(stdscr, snakeGame):
        stdscr.erase()
        stdscr.box()
        maxY, maxX = stdscr.getmaxyx()
        text = "Resize the screen"
        y = int((maxY - 1) / 2)
        x = int((maxX - len(text)) / 2)
        if (x <= 0 or y <= 0):
            raise ExitTotal("Screen is too small")
        stdscr.addstr(y, x, text)
        stdscr.refresh()
        time.sleep(0.2)
    stdscr.erase()

def setCursesLogic():
    # curses.resizeterm(26, 51)

    curses.curs_set(0)  # Make cursor invisilble

    curses.init_pair(10, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)  # Player 1
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Player 2
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)  # Player 3
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_YELLOW)  # Player 4

    # Letters title
    curses.init_pair(15, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(16, curses.COLOR_RED, curses.COLOR_CYAN)
    curses.init_pair(17, curses.COLOR_RED, curses.COLOR_GREEN)
    curses.init_pair(18, curses.COLOR_RED, curses.COLOR_YELLOW)
    curses.init_pair(19, curses.COLOR_RED, curses.COLOR_MAGENTA)


def handleGame(snakeGame):
    global PAUSED

    controller = Controller(len(snakeGame.snakes))
    curKey = -1
    start = time.time()
    while True:
        if (checkIfEnoughSpaceForGame(FULL_SCREEN, snakeGame)):
            raise NotEnoughSpace("Current max: {0}, Needed space: {1}".format(
                "x: {0} y: {1}".format(FULL_SCREEN.getmaxyx()[1], FULL_SCREEN.getmaxyx()[0]),
                "x: {0} y: {1}".format(snakeGame.sizeX, snakeGame.sizeY)))

        if (snakeGame.allDead()):
            break
        try:
            newKey = FULL_SCREEN.getch()
        except(curses.error):
            newKey = -1
        if (newKey != -1):
            curKey = newKey

        directions = controller.keypressed(curKey)
        if (directions != -1):
            snakeGame.changeDirections(directions[0], directions[1])

        if (curKey == curses.KEY_HOME or curKey == ord("z")):
            PAUSED = True
            pauseWindowOut = pauseGameWindow()
            if (pauseWindowOut == Actions.Restart):
                snakeGame.restart()
            curKey = -1
        elapsed = time.time() - start
        if (elapsed >= 0.30 and not PAUSED):
            start = time.time()
            snakeGame.tick()
            printScreen(snakeGame.getScreenRepr())
        printStats(snakeGame.getStatsRepr())


def pauseGameWindow():
    global MAP_SCREEN
    maxY, maxX = MAP_SCREEN.getmaxyx()
    sizeX = 20
    sizeY = 10
    cordX =  int((maxX - sizeX) / 2)
    cordY = int((maxY - sizeY) / 2)
    if(cordX <= 0 or cordY <= 0):
        raise Exception("The screen of the game is too little for the pause menu")

    pauseWindow = curses.newwin(sizeY, sizeX, cordY, cordX)
    pauseWindow.clear()

    pauseWindow.box()
    pauseWindow.hline(2, 1, curses.ACS_HLINE, sizeX - 2)

    title = "Pause"
    pauseWindow.addstr(1, int((sizeX - len(title))/2),
                  title,
                  curses.A_STANDOUT)

    createMenu(pauseWindow, [("Restart", restartFunc), ("Exit", exitFunc)], startX=2, startY=4)

    pauseWindow.refresh()
    try:
        returnValue = menu_handler(pauseWindow)
    except GoBackToMainScreen:
        raise GoBackToMainScreen()
    finally:
        global PAUSED
        PAUSED = False
        pauseWindow.erase()


    return returnValue

def restartFunc():
    return  Actions.Restart

def exitFunc():
    raise GoBackToMainScreen()



class Actions(object):
    Restart = "restart"


if(__name__ == "__main__"):
    try:
        wrapper(main)
    except ExitTotal as err:
        print("Game exited: ")
        print(err)
