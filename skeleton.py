import pygame
import random
from enemy import Enemy
from assets import GAME_ASSETS

class Skeleton(Enemy):
    # attributes
    __attackList = None
    __previousAttack = None

    # end attributes

    def __init__(self, position, window):
        super().__init__("Skeleton", GAME_ASSETS['skeleton'], position, window, 80, 90, 50, 50)
        self.setImage(pygame.transform.scale(self.getImage(), [40,30]))
        self.__attackList = {
            "Punch": self.punch,
            "Death Bolt": self.deathBolt,
            "Curse": self.curse
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
    def move(self):
        position = self.getPosition()
        window = self.getWindow()
        image = self.getImage()
        
        # Move the skeleton randomly within a specified range
        position[0] += random.randint(-15, 15)  # Move horizontally
        position[1] += random.randint(-15, 15)  # Move vertically

        # Ensure the skeleton stays within the bounds of the window
        position[0] = max(0, min(window.get_width() - image.get_width(), position[0]))  # Limit horizontal movement
        position[1] = max(0, min(window.get_height() - image.get_height(), position[1]))  # Limit vertical movement
        self.setPosition(position)

    def attack(self, target):
        attackRoll = random.randint(0, 100)

        if 0 < attackRoll <= 60:
            selectedAttack = "Punch"
        elif 60 < attackRoll <= 70 and self.getPreviousAttack() == "Punch" and not target.getCursedStatus()["status"]:
            selectedAttack = "Curse"
        else:
            selectedAttack = "Death Bolt"

        self.__attackList[selectedAttack](target)
        self.setPreviousAttack(selectedAttack)

    # attacks
    def punch(self, player):
        damage = (self.getStrength() + 10) * player.getDefenseMultiplier()
        print(f"{self.getName()} punches {player.getName()} for {damage} damage! \n")
        player.takeDamage(damage)

    def deathBolt(self, player):
        damage = (self.getMagicPower() + 30) * player.getMagicResistance()
        print(f"{self.getName()} fires a death bolt at {player.getName()} for {damage} damage! \n")
        player.takeDamage(damage)

    def curse(self, player):
        damage = self.getMagicPower()
        turnDelay = 2
        player.setCursedStatus(True, turnDelay, damage)
        print(f"{self.getName()} lays a curse upon {player.getName()} for {turnDelay} turns!")

    # Game features
    
    def takeDamage(self, damage):
        self.setCurrentHP(self.getCurrentHP() - damage)
        print(f"{self.getName()} has {self.getCurrentHP()} HP remaining")

    def draw(self, newPosition, scaleFactor):
        # Draw the skeleton image on the window at the current position

        if newPosition: # check if a different position is specified for the skeleton to be drawn at
            position = newPosition # use the new position instead.
        else:
            position = self.getPosition() # if no new position is given, it uses its current position instead

        image = pygame.transform.scale(self.getImage(), (self.getImage().get_width() * scaleFactor, self.getImage().get_height() * scaleFactor)) # Resizes the image to be drawn based on the scale factor

        self.getWindow().blit(image, position)
