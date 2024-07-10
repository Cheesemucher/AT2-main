import pygame
import random
from assets import GAME_ASSETS
from enemy import Enemy

class Goblin(Enemy):
    #attributes
    __attackList = None
    __previousAttack = None
    #end attributes

    def __init__(self, position, window): 
        super().__init__(GAME_ASSETS["goblin"], position, window, pygame.image.load("AT2/assets/goblin.png").convert_alpha(), 80, 95, 60, None)
        # Load the goblin image from the specified path
        self.__attackList = {
            "Stab" : self.stab,
            "Claw" : self.claw,
            "Bite" : self.bite
        }

    #accessors
    def getImage(self):
        return self.__image

    def getAttackList(self):
        return self.__attackList

    def getPreviousAttack(self):
        return self.__previousAttack


    #mutators
    def setImage(self, newImage):
        self.__image = newImage

    def setAttackList(self, newAttackList):
        self.__attackList = newAttackList

    def setPreviousAttack(self, newPreviousAttack):
        self.__previousAttack = newPreviousAttack


    #behaviours

    def attack(self, target):
        if self.getPreviousAttack() != "Stab" and random.randint(0,5) != 0: #just to throw in some probability so it doesnt do stab every second turn
            selectedAttack = "Stab"
        else:
            attackRoll = random.randint(0, 100)
            if 0 < attackRoll <= 55:
                selectedAttack = "Claw"
            elif 55 <= 90:
                selectedAttack = "Bite"
            else:
                selectedAttack = "Stab"

        self.__attackList[selectedAttack](target)
        self.setPreviousAttack(selectedAttack)

    def stab(self, player):
        damage = (self.getStrength() + 10) * player.getDefenseMultiplier()
        print(f"{self.getName()} stabs {player.getName()} for {damage} damage! \n")
        player.takeDamage(damage)

    def bite(self, player):
        damage = (self.getStrength() * 1.1) * player.getDefenseMultiplier()
        print(f"{self.getName()} bites {player.getName()} for {damage} damage! \n")
        player.takeDamage(damage)

    def claw(self, player):
        damage = (self.getStrength() - 10) * player.getDefenseMultiplier()
        print(f"{self.getName()} claws {player.getName()} for {damage} damage! \n")
        player.takeDamage(damage)

    def move(self):
        # Move the goblin randomly within a specified range
        self.position[0] += random.randint(-10, 10)  # Randomly change the x-coordinate
        self.position[1] += random.randint(-10, 10)  # Randomly change the y-coordinate

        # Ensure the goblin stays within the bounds of the window
        self.position[0] = max(0, min(self.window.get_width() - self.image.get_width(), self.position[0]))  # Clamp the x-coordinate
        self.position[1] = max(0, min(self.window.get_height() - self.image.get_height(), self.position[1]))  # Clamp the y-coordinate

    def draw(self):
        # Draw the goblin on the game window
        self.window.blit(self.image, self.position)
    
    def takeDamage(self, damage):
        self.setCurrentHP(self.getCurrentHP() - damage)
        print(f"{self.getName()} has {self.getCurrentHP()} HP remaining")
