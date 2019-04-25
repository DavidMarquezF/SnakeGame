import time

class PlayerStats(object):
    def __init__(self, startLives, countDown = 5):
        self.isDead = False
        self.timeAlive= 0
        self.foodEaten= 0
        self.deaths = 0
        self.snakesKilled = 0
        self.lives = startLives
        self.startLives = startLives
        self.startTimeAlive = time.time()
        self.countDownResurrectStart = 0
        self.countDown = countDown

    def eatFood(self):
        self.foodEaten +=1

    def die(self):
        self.countDownResurrectStart = time.time()
        self.deaths +=1
        self.isDead = True

    def resurrect(self):
        self.isDead = False
        self.restartFood()
        self.restartTimer()

    def killedSnake(self):
        self.snakesKilled +=1


    def restartTimer(self):
        self.timeAlive = 0
        self.startTimeAlive = time.time()

    def restartFood(self):
        self.foodEaten = 0

    def restartSnakesKilled(self):
        self.snakesKilled = 0

    def restartAll(self):
        self.deaths = 0
        self.lives = self.startLives
        self.isDead = False
        self.restartFood()
        self.restartSnakesKilled()
        self.restartTimer()

    def getTimeAlive(self):
        if(not self.isDead):
            self.timeAlive =  time.time() - self.startTimeAlive
        return round (self.timeAlive,1)

    def getCountDown(self):
        if (self.lives > 0 and self.isDead):
            elapsedTimeSinceDeath = time.time() - self.countDownResurrectStart
            rounded = round(self.countDown - elapsedTimeSinceDeath,1)
            return rounded if rounded > 0 else 0

        return self.countDown
