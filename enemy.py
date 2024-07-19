import pygame
import random
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


# behaviours
    def isAlive(self):
        return self.getCurrentHP() > 0

    @abstractmethod
    def takeDamage(self, damage):
        # Reduce the enemy's health by the specified damage amount
        pass

    @abstractmethod
    def draw(self):
        # Adjust the position to ensure the image does not overflow the window boundaries
        adjustedPosition = [
        max(0, min(self.__window.get_width() - self.__image.get_width(), self.__position[0])),
        max(0, min(self.__window.get_height() - self.__image.get_height(), self.__position[1]))
        ]

        # Draw the enemy image on the window at the adjusted position
        self.__window.blit(self.__image, adjustedPosition)
