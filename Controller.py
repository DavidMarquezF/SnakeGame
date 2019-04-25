import curses
from Snake import  Directions
P1 = {ord("w"): Directions.up, ord("s"):Directions.down, ord("d"):Directions.right, ord("a"):Directions.left}
P2 = {curses.KEY_UP: Directions.up, curses.KEY_DOWN:Directions.down, curses.KEY_RIGHT:Directions.right, curses.KEY_LEFT:Directions.left}
P3 = {ord("u"): Directions.up, ord("j"):Directions.down, ord("k"):Directions.right, ord("h"):Directions.left}
P4 = {ord("8"): Directions.up, ord("5"):Directions.down, ord("6"):Directions.right, ord("4"):Directions.left} #Num Block must be off to use the numPad

class Controller(object):
    maxPlayers = 4
    def __init__(self, players = 1):
        if players > Controller.maxPlayers:
            raise Exception("Too many players")
        self.players = players

    def changePlayerNum(self, players):
        self.players = players
    def keypressed(self, key):
        if key in P1:
            return [1, P1[key]]

        if key in P2:
            return  [2 if self.players > 1 else 1, P2[key]]

        if key in P3:
            if self.players > 2:
                return [3, P3[key]]
            elif self.players > 1 and self.players < 3:
                return -1
            else:
                return  [1, P3[key]]
        if key in P4:
            if self.players > 3:
                return [4, P4[key]]
            else:
                return -1


        return -1
