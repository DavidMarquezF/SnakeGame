from Snake import *
import random
import math

heartSymbol= "♥"#u"\u2661"

class Collision(object):
    WALL = "wall"
    SNAKE = "snake"
    NONE = "none"
    SELF = "self"
    FOOD="food"
    HEART="heart"
    def __init__(self, collisionType, collisionTo = None):
        self.collisionType = collisionType
        self.collisonTo = collisionTo


class SnakeGame(object):
    def __init__(self):
        Snake.PlayerNum = 1
        self.sizeX = 50
        self.sizeY = 25

        self.maxFood = int(self.sizeX * self.sizeY * 0.03)
        if(self.maxFood < 10):
            self.maxFood = 10

        self.screen=[]
        self.__setScreenBlank()
        self.snakes = []
        self.food = []
        self.hearts = []

    def __setScreenBlank(self):
        lines = []

        for y in range(self.sizeY):
            lines.append([" " for i in range(self.sizeX )])
        self.screen = lines

    def addSnake(self, name):
        self.snakes.append(Snake(name, self.getRandPos))

    def getRandPos(self, snake):
        percentageX = int(self.sizeX * 0.1)
        percentageY = int(self.sizeY * 0.1)

        startLength = snake.startParts

        while True:
            randx = random.randint(percentageX, self.sizeX - percentageX)
            randy = random.randint(percentageY, self.sizeY - percentageY)

            #TODO: Mirar que les posicions de comencar no toquin ni a la banda ni a cap snake

            correctPos = True
            for snak in self.snakes:
                if snak == snake:
                    continue
                if([randx, randy] in snak.getPositions()):
                    correctPos = False
                    break

            if(correctPos):
                break

        return [randx, randy]

    def changeDirections(self, playerNum, dir):
        self.snakes[playerNum -1].changeDirection(dir)

    def tick(self):
        for snake in self.snakes:
            snake.tick()

        snakeToDie=[]
        snakeToAdd=[]
        for snake in self.snakes:
            if not snake.isAlive():
                continue
            collision=self.__checkCollision(snake)
            if(collision.collisionType == Collision.WALL or collision.collisionType == Collision.SELF):
                snakeToDie.append(snake)
            elif collision.collisionType == Collision.SNAKE:
                snakeToDie.append(snake)
                collision.collisonTo.stats.killedSnake()
            elif(collision.collisionType == Collision.FOOD):
                self.food.remove(collision.collisonTo)
                snakeToAdd.append(snake)
            elif(collision.collisionType == Collision.HEART):
                snake.stats.lives += 1
                self.hearts.remove(collision.collisonTo)

        for snake in snakeToAdd:
            snake.stats.eatFood()
            snake.addPart()
        for snake in snakeToDie:
            for snakePos in snake.getPositions()[1:]:
                self.food.append(snakePos)
            snake.die()

        #Spawn food
        if(len(self.food) < self.maxFood):
            for i in range(random.randint(0,2)):
                if (len(self.food) >= self.maxFood):
                    break
                if(random.randint(0, 100) > 90):
                    self.spawnObject("food")
        if(random.randint(0,100) > 99):
            self.spawnObject("heart")

        self.__actualizeScreen()


    def spawnObject(self, type):
        while True:
            percentageX = math.ceil(self.sizeX * 0.07)
            randx = random.randint(percentageX, self.sizeX - percentageX)

            percentageY = math.ceil(self.sizeY * 0.07)
            randy = random.randint(percentageY, self.sizeY - percentageY)

            if(randx == 0):
                randx = 1
            elif randx == self.sizeX:
                randx = self.sizeX - 1

            if(randy == 0):
                randy = 1
            elif randy == self.sizeY:
                randy = self.sizeY - 1

            position = [randx, randy]
            if(position not in self.food and position not in self.hearts):
                br = True
                for snake in self.snakes:
                    if(position in snake.getPositions()):
                        br = False
                if br:
                    break

        if(type == "food"):
            self.food.append([randx,randy])
        elif(type == "heart"):
            self.hearts.append([randx, randy])
        else:
            raise NotImplemented("Type {} not implemented".format(type))

    def __actualizeScreen(self):
        self.__setScreenBlank()
        for food in self.food:
            self.screen[food[1]][food[0]] = "*"
        for heart in self.hearts:
            self.screen[heart[1]][heart[0]] = heartSymbol
        for snake in self.snakes:
            if not snake.isAlive():
                continue
            for part in snake.parts:
                position = part.getPos()
                curRep = "part"+str(snake.playerNum)
                if (part == snake.getHeadPart()):
                    curRep = "head"+ str(snake.playerNum)

                if(position[1] > self.sizeY-1 or position[0] > self.sizeX-1):
                    raise IndexError("Max size {0}, Current expected pos: {1}".format("[{0}, {1}]".format(self.sizeX, self.sizeY), "[{0}, {1}]".format(position[0], position[1])))
                self.screen[position[1]][position[0]] =curRep


    def getScreenRepr(self):
        return self.screen

    def getStatsRepr(self):
        return {snake.name : snake.stats for snake in self.snakes}

    def allDead(self):
        for snake in self.snakes:
            if(snake.isAlive() or snake.stats.lives > 0):
                return False
        return True

    def __checkCollision(self, snake):
        headPos = snake.getHeadPart().getPos()
        if(headPos[0] >= self.sizeX or headPos[0] < 0):
            return Collision(Collision.WALL)
        if(headPos[1] >= self.sizeY or headPos[1] < 0):
            return Collision(Collision.WALL)

        for snakeColl in self.snakes:
            if headPos in snakeColl.getPositions():
                if snakeColl == snake:
                    if(headPos in snake.getPositions()[1:]):
                        return Collision(Collision.SELF)
                else:
                    return Collision(Collision.SNAKE, snakeColl)

        if(snake.getHeadPart().getPos() in self.food):
            return Collision(Collision.FOOD, collisionTo=snake.getHeadPart().getPos())
        elif(snake.getHeadPart().getPos() in self.hearts):
            return Collision(Collision.HEART, collisionTo=snake.getHeadPart().getPos())


        return Collision(Collision.NONE)

    def restart(self):
        self.food = []
        self.hearts=[]
        for snake in self.snakes:
            snake.start(True)


