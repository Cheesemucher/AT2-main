from enemy import Enemy
import pygame
import random

class Skeleton(Enemy):
    #attributes
    __attackList = None
    __previousAttack = None
    #__image = pygame.image.load("AT2/assets/skeleton.png").convert_alpha()
    #end attributes

    def __init__(self, position, window):
        super().__init__("Skeleton", position, window, pygame.image.load("AT2/assets/skeleton.png").convert_alpha(), 80, 90, 50, 50) 
        
        self.__attackList = {
            "Punch" : self.punch,
            "Death Bolt" : self.deathBolt,
            "Curse" : self.curse
        }

        #self.position = position  # Store the initial position of the skeleton
        #self.window = window  # Store the window object where the skeleton will be drawn


    #accessors
    def getAttackList(self):
        return self.__attackList

    def getPreviousAttack(self):
        return self.__previousAttack

    def getImage(self):
        return self.__image


    #mutators
    def setAttackList(self, newAttackList):
        self.__attackList = newAttackList

    def setPreviousAttack(self, newPreviousAttack):
        self.__previousAttack = newPreviousAttack

    def setImage(self, newImage):
        self.__image = newImage




    #behaviours

    def move(self):
        # Move the skeleton randomly within a specified range
        self.position[0] += random.randint(-15, 15)  # Move horizontally
        self.position[1] += random.randint(-15, 15)  # Move vertically

        # Ensure the skeleton stays within the bounds of the window
        self.position[0] = max(0, min(self.window.get_width() - self.image.get_width(), self.position[0]))  # Limit horizontal movement
        self.position[1] = max(0, min(self.window.get_height() - self.image.get_height(), self.position[1]))  # Limit vertical movement

    def draw(self):
        # Draw the skeleton image on the window at the current position
        self.window.blit(self.image, self.position)

            
    def attack(self, target):
        
        attackRoll = random.randint(0, 100)

        if 0 < attackRoll <= 60:
            selectedAttack = "Punch"
        elif 60 < attackRoll <= 70 and self.getPreviousAttack() == "Punch" and target.getCursedStatus()["status"] == False:
            selectedAttack = "Curse"
        else:
            selectedAttack = "Death Bolt"

        #self.getAttackList()[selectedAttack](target)
        self.curse(target)
        self.setPreviousAttack(selectedAttack)

    #attacks
    def punch(self, player):
        damage = (self.getStrength() + 10) * player.getDefenseMultiplier()
        print(f"{self.getName()} punches {player.getName()} for {damage} damage! \n")
        player.takeDamage(damage)

    def deathBolt(self, player):
        damage = (self.getMagicPower() + 30) * player.getMagicResistnce()
        print(f"{self.getName()} fires a death bolt at {player.getName()} for {damage} damage! \n")
        player.takeDamage(damage)

    def curse(self, player):
        damage = self.getMagicPower()
        turnDelay = 2
        player.setCursedStatus(True, turnDelay, damage)

        print(f"{self.getName()} lays a curse upon {player.getName()} for {turnDelay} turns!")

    def takeDamage(self, damage):
        self.setCurrentHP(self.getCurrentHP() - damage)
        print(f"{self.getName()} has {self.getCurrentHP()} HP remaining")