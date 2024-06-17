import pygame
import random

class Enemy:
    #attributes
    __image = None
    __position = None
    __window = None
    __defenseMultiplier = None # % of physical damage that will be recieved on hit
    __magicResistanceMultiplier = None # % of magic damage that will be recieved on hit
    __maxHP = None
    __currentHP = None 
    #end attributes


    #constructors
    def __init__(self, imagePath, position, window, defenseMultiplier, magicResistanceMultiplier):
        # Load the enemy image from the specified image path
        self.__image = pygame.image.load(imagePath).convert_alpha()

        # Scale the enemy image to 0.75 times the original size
        self.__image = pygame.transform.scale(self.__image, (int(self.__image.get_width() * 0.75), int(self.__image.get_height() * 0.75)))
        
        # Set the initial position of the enemy
        self.__position = position

        self.__window = window
        self.__defenseMultiplier = defenseMultiplier
        self.__magicResistanceMultiplier = magicResistanceMultiplier
        self.__maxHP = 100
        self.__currentHP = self.__maxHP

#accessors
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


#mutators
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


# behaviours
    def takeDamage(self, damage):
        # Reduce the enemy's health by the specified damage amount
        self.setCurrentHP(self.__currentHP - damage)

        # Return True if the enemy's health is less than or equal to 0, indicating that it is defeated
        return self.__currentHP <= 0

    def draw(self):
        # Adjust the position to ensure the image does not overflow the window boundaries
        adjustedPosition = [
        max(0, min(self.__window.get_width() - self.__image.get_width(), self.__position[0])),
        max(0, min(self.__window.get_height() - self.__image.get_height(), self.__position[1]))
        ]

        # Draw the enemy image on the window at the adjusted position
        self.__window.blit(self.__image, adjustedPosition)
