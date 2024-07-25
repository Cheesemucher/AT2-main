import pygame
import random
from bar import Bar
from abc import ABC, abstractmethod

class Enemy:
    #attributes
    __name = None
    __image = None
    __position = None
    __window = None
    __defenseMultiplier = None # % of physical damage that will be recieved on hit
    __magicResistanceMultiplier = None # % of magic damage that will be recieved on hit
    __maxHP = None
    __currentHP = None 
    __strength = None
    __magicPower = None
    __level = None
    __enemy_health_bar = None
    #end attributes


    #constructors
    def __init__(self, name, image, position, window, defenseMultiplier, magicResistanceMultiplier, strength, magicPower, maxHP, level):

        self.__window = window
        self.__position = position
        self.__image = pygame.image.load(image).convert_alpha()
        self.__name = name
        self.__defenseMultiplier = defenseMultiplier/100
        self.__magicResistanceMultiplier = magicResistanceMultiplier/100
        self.__maxHP = maxHP
        self.__currentHP = self.__maxHP
        self.__strength = strength
        self.__magicPower = magicPower
        self.__level = level
        self.__enemy_health_bar = Bar(window, self, (3/4 * window.get_width() - 10,10), "HP") # Bar object that tracks enemy HP

#accessors
    def getName(self):
        return self.__name
    
    def getImage(self):
        return self.__image

    def getPosition(self):
        return self.__position

    def getWindow(self):
        return self.__window

    def getDefenseMultiplier(self):
        return self.__defenseMultiplier

    def getMagicResistanceMultiplier(self):
        return self.__magicResistanceMultiplier

    def getMaxHP(self):
        return self.__maxHP

    def getCurrentHP(self):
        return self.__currentHP

    def getStrength(self):
        return self.__strength
    
    def getMagicPower(self):
        return self.__magicPower
    
    def getLevel(self):
        return self.__level
    
    def getEnemyHealthBar(self):
        return self.__enemy_health_bar


#mutators
    def setName(self, newName):
        self.__name = newName

    def setImage(self, newImage):
        self.__image = newImage

    def setPosition(self, newPosition):
        self.__position = newPosition

    def setWindow(self, newWindow):
        self.__window = newWindow

    def setDefenseMultiplier(self, newDefenseMultiplier):
        self.__defenseMultiplier = newDefenseMultiplier

    def setMagicResistanceMultiplier(self, newMagicResistanceMultiplier):
        self.__magicResistanceMultiplier = newMagicResistanceMultiplier

    def setMaxHP(self, newMaxHP):
        self.__maxHP = newMaxHP

    def setCurrentHP(self, newCurrentHP):
        self.__currentHP = newCurrentHP
    
    def setStrength(self, newStrength):
        self.__strength = newStrength
    
    def setMagicPower(self, newMP):
        self.__magicPower = newMP

    def setLevel(self, newLevel):
        self.__level = newLevel

    def setEnemyHealthBar(self, healthBar):
        self.__enemy_health_bar = healthBar

# behaviours
    def isAlive(self):
        return self.getCurrentHP() > 0

    def takeDamage(self, damage):
        output = []
        self.setCurrentHP(self.getCurrentHP() - damage)
        output.append(f"{self.getName()} has {self.getCurrentHP()} HP remaining")

        self.__enemy_health_bar.update_quantity()
        return output

    @abstractmethod
    def draw(self):
        pass
