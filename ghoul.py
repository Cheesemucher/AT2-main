import pygame
import random
from assets import GAME_ASSETS
from enemy import Enemy

class Ghoul(Enemy):
    # attributes
    __attackList = None
    __previousAttack = None
    __XpValue = None

    # end attributes

    def __init__(self, position, window, level):

        # Assigning skill points
        defenseMultiplier = 90
        magicResistanceMultiplier = 70
        strength = 10
        magicPower = 60
        maxHP = 100

        points = 3 * level # Gets 3 attribute points to assign per level
        while points > 0:
            skillRNG = random.randint(1,5) #randomly assigns attribute points
            if skillRNG == 1:
                defenseMultiplier -= 1
            elif skillRNG == 2:
                magicResistanceMultiplier -= 1
            elif skillRNG == 3:
                strength += 1
            elif skillRNG == 4:
                magicPower += 3
            else:
                maxHP += 5
            points -= 1
            
        super().__init__("Ghoul", GAME_ASSETS['ghoul'], position, window, defenseMultiplier, magicResistanceMultiplier, strength, magicPower, maxHP, level)
        self.setImage(pygame.transform.scale(self.getImage(), [40, 30]))
        self.__attackList = {
            "Headbut": self.headbutt,
            "Death Bolt": self.deathBolt,
            "Expose": self.expose,
            "Curse": self.curse
        }
        self.__XpValue = 120 + 5 * level

    # accessors
    def getAttackList(self):
        return self.__attackList

    def getPreviousAttack(self):
        return self.__previousAttack
    
    def getXpValue(self):
        return self.__XpValue

    # mutators
    def setAttackList(self, newAttackList):
        self.__attackList = newAttackList

    def setPreviousAttack(self, newPreviousAttack):
        self.__previousAttack = newPreviousAttack

    def setXpValue(self, newXP_value):
        self.__previousAttack = newXP_value

    # behaviours
    def move(self):
        position = self.getPosition()
        window = self.getWindow()
        image = self.getImage()
        
        # Move the ghoul randomly within a specified range
        position[0] += random.randint(-15, 15)  # Move horizontally
        position[1] += random.randint(-15, 15)  # Move vertically

        # Ensure the ghoul stays within the bounds of the window
        position[0] = max(0, min(window.get_width() - image.get_width(), position[0]))  # Limit horizontal movement
        position[1] = max(0, min(window.get_height() - image.get_height(), position[1]))  # Limit vertical movement
        self.setPosition(position)

    def attack(self, target):
        attackRoll = random.randint(0, 100)

        if 0 < attackRoll <= 30:
            selectedAttack = "Headbut"
        elif 30 < attackRoll <= 60 and not target.getExposedStatus():
            selectedAttack = "Expose"
        elif self.__previousAttack == "Headbut":
            selectedAttack = "Curse"
        else:
            selectedAttack = "Death Bolt"

        attack_output = self.__attackList[selectedAttack](target)
        self.setPreviousAttack(selectedAttack)
        return attack_output

    # attacks
    def headbutt(self, player):
        output = []
        damage = (self.getStrength() + 10) * player.getDefenseMultiplier()
        output.append(f"{self.getName()} headbutts {player.getName()} for {damage} damage! \n")
        damage_output = player.takeDamage(damage)
        output.extend(damage_output)
        return output

    def deathBolt(self, player):
        output = []
        damage = (self.getMagicPower() + 30) * player.getMagicResistance()
        output.append(f"{self.getName()} fires a death bolt at {player.getName()} for {damage} damage! \n")
        damage_output = player.takeDamage(damage)
        output.extend(damage_output)
        return output

    def curse(self, player):
        output = []
        damage = self.getMagicPower()
        turnDelay = 2
        player.setCursedStatus(True, turnDelay, damage)
        output.append(f"{self.getName()} lays a curse upon {player.getName()} for {turnDelay} turns!")
        return output
    
    def expose(self, player):
        output = []
        player.setExposedStatus(True, 2)
        output.append(f"{self.getName()} casts an exposing spell upon {player.getName()} for 2 turns!")
        return output

    # Game features
    
    def takeDamage(self, damage):
        output = []
        self.setCurrentHP(self.getCurrentHP() - damage)
        output.append(f"{self.getName()} has {self.getCurrentHP()} HP remaining")
        return output

    def draw(self, newPosition, scaleFactor):
        ''' Draw the ghoul image on the window at the current position'''
        # Generate a random position if this class has no position currently 
        if not self.getPosition():
            startingX = random.randint(100, self.getWindow().get_width() - 100)
            startingY = random.randint(100, self.getWindow().get_height() - 100)
            self.setPosition((startingX, startingY))

        if newPosition: # check if a different position is specified for the ghoul to be drawn at
            position = newPosition # use the new position instead.
        else:
            position = self.getPosition() # if no new position is given, it uses its current position instead

        image = pygame.transform.scale(self.getImage(), (self.getImage().get_width() * scaleFactor, self.getImage().get_height() * scaleFactor)) # Resizes the image to be drawn based on the scale factor

        self.getWindow().blit(image, position)
