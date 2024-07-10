from character import Character
from game import Game
import pygame, sys

class healthBar():
    #attributes
    __currentHP = None
    __maxHP = None
    __barLength = None
    __maxtolengthRatio = None
    #end attributes

    def __init__(self):
        self.__maxHP = Character.getMaxHP()
        self.__currentHP = Character.getCurrentHP()
        self.__barLength = 400
        self.__maxtolengthRatio = self.maxHP / self.barLength

    #accessors
    def getCurrentHP(self):
        return Character.getCurrentHP()

    def getMaxHP(self):
        return Character.getMaxHP()

    def getBarLength(self):
        return self.__barLength

    def getMaxtolengthRatio(self):
        return self.__maxtolengthRatio


    #mutators
    def setCurrentHP(self, newCurrentHP):
        self.__currentHP = newCurrentHP

    def setMaxHP(self, newMaxHP):
        self.__maxHP = newMaxHP

    def setBarLength(self, newBarLength):
        self.__barLength = newBarLength

    def setMaxtolengthRatio(self, newMaxtolengthRatio):
        self.__maxtolengthRatio = newMaxtolengthRatio




    #def loseHP(self, amount):
      #  if self.curren

    def healthBar(self):
        pygame.draw.rect(Game.get_window(), (255,0,0),(10,10,self.getCurrentHP()/self.getMaxtolengthRatio(),25))
        pygame.draw.rect(Game.get_window(), (255,255,255), (10,10,self.getBarLength,25), 4)