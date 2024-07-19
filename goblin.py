import pygame
import random
from assets import GAME_ASSETS
from enemy import Enemy

class Goblin(Enemy):
    # attributes
    __attackList = None
    __previousAttack = None

    # end attributes

    def __init__(self, position, window, level):
        defenseMultiplier = 80
        magicResistanceMultiplier = 95
        strength = 60
        maxHP = 100

        points = 3 * level
        while points > 0:
            skillRNG = random.randint(1,4)
            if skillRNG == 1:
                defenseMultiplier -= 1
            elif skillRNG == 2:
                magicResistanceMultiplier -= 1
            elif skillRNG == 3:
                strength += 2
            else:
                maxHP += 5
            points -= 1

        super().__init__('Goblin', GAME_ASSETS['goblin'], position, window, defenseMultiplier, magicResistanceMultiplier, strength, None, maxHP, level)
        # Load the goblin image from the specified path
        self.setImage(pygame.transform.scale(self.getImage(), [40,30]))
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
        output = []

        if self.getPreviousAttack() != "Stab" and random.randint(0, 5) != 0:  # just to throw in some probability so it doesn't do stab every second turn
            selectedAttack = "Stab"
        else:
            attackRoll = random.randint(0, 100)
            if 0 < attackRoll <= 55:
                selectedAttack = "Claw"
            elif 55 <= 90:
                selectedAttack = "Bite"
            else:
                selectedAttack = "Stab"

        attackOutput = self.__attackList[selectedAttack](target)
        output.extend(attackOutput)
        self.setPreviousAttack(selectedAttack)

        return output

    def stab(self, player):
        output = []

        damage = (self.getStrength() + 10) * player.getDefenseMultiplier()
        output.append(f"{self.getName()} stabs {player.getName()} for {damage} damage!")
        output.extend(player.takeDamage(damage))

        return output

    def bite(self, player):
        output = []

        damage = (self.getStrength() * 1.1) * player.getDefenseMultiplier()
        output.append(f"{self.getName()} bites {player.getName()} for {damage} damage!")
        output.extend(player.takeDamage(damage))

        return output

    def claw(self, player):
        output = []

        damage = (self.getStrength() - 10) * player.getDefenseMultiplier()
        output.append(f"{self.getName()} claws {player.getName()} for {damage} damage!")
        output.extend(player.takeDamage(damage))

        return output

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

    def draw(self, newPosition, scaleFactor):
        # Draw the skeleton image on the window at the current position

        if newPosition: # check if a different position is specified for the skeleton to be drawn at
            position = newPosition # use the new position instead.
        else:
            position = self.getPosition() # if no new position is given, it uses its current position instead

        image = pygame.transform.scale(self.getImage(), (self.getImage().get_width() * scaleFactor, self.getImage().get_height() * scaleFactor)) # Resizes the image to be drawn based on the scale factor

        self.getWindow().blit(image, position)

    def takeDamage(self, damage):
        output = []
        self.setCurrentHP(self.getCurrentHP() - damage)
        output.append(f"{self.getName()} has {self.getCurrentHP()} HP remaining")

        return output
