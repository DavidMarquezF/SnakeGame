from Stats import PlayerStats
import time
#from enum import Enum
#class Directions(object):#Enum): #TODO: Existeix python Enum l'unic que s'ha d'intalar el pip. QUan funcioni ja ho fare servir
    #up=0
     #down=1
    #left=2
    #right=3
class Directions(object):
    up = 0
    down=1
    left=2
    right=3
    def getInverse(self, dir):
        inverse = {
            Directions.up: Directions.down,
            Directions.down: Directions.up,
            Directions.right: Directions.left,
            Directions.left:Directions.right
        }

        return inverse[dir]



class Snake(object):
    PlayerNum=1
    def __init__(self, name, randPosFunc, curDir = Directions.right, startParts = 2, startLives=3):
        self.playerNum = Snake.PlayerNum
        Snake.PlayerNum +=1
        self.name = name
        self.parts = []
        self.curDir = curDir
        self._nextDir = curDir
        self.startParts = startParts
        self.stats = PlayerStats(startLives=startLives, countDown=5)
        self.stats.lives = startLives
        self.getRandPosFunc = randPosFunc
        self.start()


    def start(self, restart = False):
        self.parts=[]
        pos = self.getRandPosFunc(self)
        self.parts.append(SnakePart(pos[0], pos[1], self.curDir))
        for i in range(self.startParts):
            self.addPart()
        self.stats.resurrect()
        self.__alive = True
        if (restart):
            self.stats.restartAll()

    def changeDirection(self, dir):
        if not self.isAlive():
            return
        if (Directions().getInverse(dir) != self.curDir):
            self._nextDir = dir

    def tick(self):
        #Goes from tail to head so updateDirection applies after the tick
        if(not self.__alive):
            if(self.stats.lives > 0):
                if(self.stats.getCountDown() <= 0):
                    self.start()
                    self.stats.lives -= 1
            return
        if (Directions().getInverse(self._nextDir) != self.curDir):
            self.curDir = self._nextDir
            self.getHeadPart().changeDirection(self.curDir)  # TODO: Actualment si es canvia massa rapid cap una direccio i despres cap a la contraria xoca contra ell mateix

        for part in self.parts[::-1]:
            part.tick()

    def isAlive(self):
        return self.__alive

    def die(self):
        self.stats.die()
        self.parts=[]
        self.__alive = False
        if(self.stats.lives > 0):
            self.countDownResurrectStart = time.time()


    def getHeadPart(self):
        return self.parts[0]

    def addPart(self):
        x, y = self.parts[-1].getPos()

        if self.curDir == Directions.up:
            y += 1
        elif self.curDir == Directions.down:
            y -= 1
        elif self.curDir == Directions.right:
            x -= 1
        elif self.curDir == Directions.left:
            x += 1
        nextPart = SnakePart(x,y, self.curDir)
        self.parts[-1].setNextPart(nextPart)
        self.parts.append(nextPart)

    def getPositions(self):
        return [part.getPos() for part in self.parts]

class SnakePart(object):
    def __init__(self,x,y, dir,nextPart = None):
        self.x = x
        self.y = y
        self.dir = dir
        self.__nextPart = nextPart

    def setNextPart(self, nextPart):
        if(self.__nextPart != None):
            raise Exception("Already has a next part assigned")
        self.__nextPart = nextPart

    def getPos(self):
        return [self.x, self.y]

    def tick(self):

        if self.dir == Directions.up:
            self.y -= 1
        elif self.dir == Directions.down:
            self.y += 1
        elif self.dir == Directions.right:
            self.x += 1
        elif self.dir == Directions.left:
            self.x -= 1
        else:
            raise Exception("Not a recognized direction")

        if(self.__nextPart != None):
            self.__nextPart.changeDirection(self.dir)


    def changeDirection(self, dir):
        self.dir = dir
