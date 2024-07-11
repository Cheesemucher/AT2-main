import pygame
import random
from assets import GAME_ASSETS
from enemy import Enemy

class Goblin(Enemy):
    # attributes
    __attackList = None
    __previousAttack = None

    # end attributes

    def __init__(self, position, window):
        super().__init__('Goblin', GAME_ASSETS['goblin'], position, window, 80, 95, 60, None)
        # Load the goblin image from the specified path
        self.setImage(pygame.image.load(GAME_ASSETS['goblin']).convert_alpha())
        self.__attackList = {
            "Stab": self.stab,
            "Claw": self.claw,
            "Bite": self.bite
        }

    # accessors
    def getAttackList(self):
        return self.__attackList

    def getPreviousAttack(self):
        return self.__previousAttack

    # mutators
    def setAttackList(self, newAttackList):
        self.__attackList = newAttackList

    def setPreviousAttack(self, newPreviousAttack):
        self.__previousAttack = newPreviousAttack

    # behaviours
    def attack(self, target):
        if self.getPreviousAttack() != "Stab" and random.randint(0, 5) != 0:  # just to throw in some probability so it doesnt do stab every second turn
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
        position = self.getPosition()
        window = self.getWindow()
        image = self.getImage()
        
        position[0] += random.randint(-10, 10)  # Randomly change the x-coordinate
        position[1] += random.randint(-10, 10)  # Randomly change the y-coordinate

        # Ensure the goblin stays within the bounds of the window
        position[0] = max(0, min(window.get_width() - image.get_width(), position[0]))  # Clamp the x-coordinate
        position[1] = max(0, min(window.get_height() - image.get_height(), position[1]))  # Clamp the y-coordinate
        self.setPosition(position)

    def draw(self):
        # Draw the goblin on the game window
        self.getWindow().blit(self.getImage(), self.getPosition())

    def takeDamage(self, damage):
        self.setCurrentHP(self.getCurrentHP() - damage)
        print(f"{self.getName()} has {self.getCurrentHP()} HP remaining")
