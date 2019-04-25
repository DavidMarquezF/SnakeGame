import curses
from Snake import *
import time


class SnakeLetter(object):
    def __init__(self, letter, colorNumber):
        self.colorNumber=colorNumber
        self.snake = Snake(letter, self.getStartPos, startParts=0, curDir=self.getDirections()[0])

    def getStartPos(self, snake):
        return self._getStartPos()
    def getDirections(self):
        return self._getDirections()

class SnakeTitleS(SnakeLetter):
    def _getStartPos(self):
        return [3,9]
    def _getDirections(self):
        return [Directions.right, None, None, None, Directions.up, None, None, Directions.left, None, None, None, Directions.up, None, None, Directions.right, None, None, None]

class SnakeTitleN(SnakeLetter):
    def _getStartPos(self):
        return [9,9]
    def _getDirections(self):
        return [Directions.up, None, None, None, None, None, Directions.right, None, Directions.down, None, None, Directions.right, Directions.down, None, None, Directions.right, None, Directions.up, None, None, None, None, None]

class SnakeTitleA(SnakeLetter):
    def _getStartPos(self):
        return [16,9]
    def _getDirections(self):
        return [Directions.up, None, None, Directions.right, Directions.up, None, Directions.right, Directions.up, Directions.right, Directions.down, Directions.right, Directions.down, None, Directions.right, Directions.down, None, None]

class SnakeTitleK_1(SnakeLetter):
    def _getStartPos(self):
        return [23,9]
    def _getDirections(self):
        return [Directions.up, None, None,None,None,None]

class SnakeTitleK_2(SnakeLetter):
    def _getStartPos(self):
        return [27,3]
    def _getDirections(self):
        return [Directions.down, Directions.left,None,Directions.down,Directions.left,Directions.down,Directions.right,Directions.down,Directions.right,Directions.down,Directions.right,Directions.down]

class SnakeTitleE_1(SnakeLetter):
    def _getStartPos(self):
        return [33,3]
    def _getDirections(self):
        return [Directions.left,None,None,None,Directions.down,None,None,None,None,None,Directions.right,None,None,None]

class SnakeTitleE_2(SnakeLetter):
    def _getStartPos(self):
        return [33,6]
    def _getDirections(self):
        return [Directions.left,None,None]

class SnakeTitle_Marc1(SnakeLetter):
    def _getStartPos(self):
        return [1,1]
    def _getDirections(self):
        return [Directions.right,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]


class SnakeTitle_Marc3(SnakeLetter):
    def _getStartPos(self):
        return [35,11]
    def _getDirections(self):
        return [Directions.left, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]


TITLE_WIDTH=37
TITLE_HEIGHT=12

class SnakeTitle(object):
    Screen = None

    def main(self, stdscr, startX = 0, startY=0):
        global Screen
        Screen = stdscr.subwin(TITLE_HEIGHT,TITLE_WIDTH,startY,startX)

        snakeTitles = [SnakeTitleS("S", 15), SnakeTitleN("N", 16), SnakeTitleA("A", 17),SnakeTitleK_1("K_1",18),SnakeTitleK_2("K_2",18),SnakeTitleE_1("E_1",19),SnakeTitleE_2("E_2",19),SnakeTitle_Marc1("M1",17),SnakeTitle_Marc3("M3",16)]
        counter = 0

        while True:
            lettersNotFinished = 0
            for snakeLetter in snakeTitles:
                self.printSnake(snakeLetter.snake.getPositions(), snakeLetter.colorNumber)
                directions = snakeLetter.getDirections()
                if(len(directions) <= counter):
                    continue

                lettersNotFinished += 1
                if(directions[counter] != None):
                    snakeLetter.snake.changeDirection(directions[counter])
                snakeLetter.snake.addPart()
                snakeLetter.snake.tick()


            time.sleep(0)#)0.05)
            counter+=1
            if lettersNotFinished == 0:
                break
            Screen.clear()



    def printSnake(self, snakePos, snakeNum):
        Screen.addstr(snakePos[0][1], snakePos[0][0], " ", curses.color_pair(snakeNum))
        for pos in snakePos[1:]:
            Screen.addstr(pos[1], pos[0], " ",  curses.color_pair(10))
        Screen.refresh()




