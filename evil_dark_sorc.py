import pygame
import random
from assets import GAME_ASSETS
from enemy import Enemy
from bar import Bar

class EvilSorceror(Enemy):
    # attributes
    __attackList = None
    __previousAttack = None
    __XpValue = None
    __cheeseCounter = None
    __shieldStatus = None
    __maxMana = None
    __currentMana = None
    __boss_mana_bar = None
    boss = None
    # end attributes

    def __init__(self, position, window, level):
        self.boss = True

        # Assigning skill points
        defenseMultiplier = 70
        magicResistanceMultiplier = 70
        magicPower = 100
        self.__maxMana = 400
        maxHP = 100

        points = 3 * level # Gets 3 attribute points to assign per level
        while points > 0:
            skillRNG = random.randint(1,5) #randomly assigns attribute points
            if skillRNG == 1:
                defenseMultiplier -= 1
            elif skillRNG == 2:
                magicResistanceMultiplier -= 1
            elif skillRNG == 3:
                self.__maxMana += 10
            elif skillRNG == 4:
                magicPower += 2
            else:
                maxHP += 5
            points -= 1
            
        super().__init__("Dark and Evil Sorceror Bob", GAME_ASSETS['sorceror'], position, window, defenseMultiplier, magicResistanceMultiplier, 80, magicPower, maxHP, level)
        self.setImage(pygame.transform.scale(self.getImage(), [90, 70]))
        self.__attackList = {
            "Magic Shield": self.magic_shield,
            "Unfair turn cheat": self.turn_cheat,
            "Unfair mana cheat": self.mana_cheat,
            "Unfair HP cheat" : self.HP_cheat,
            "Magic Nuclear Arsenal": self.magic_nuclear_arsenal,
            "Conjure Cheese": self.conjure_cheese,
        }
        self.__shieldStatus = False, 0
        self.__cheeseCounter = 0
        self.__XpValue = 1000
        self.__boss_mana_bar = Bar(window, self, (3/4 * window.get_width() - 10,40), "Mana") # Make a bar object to track boss mana
        self.__currentMana = self.getMaxMana()
    

    #accessors
    def getAttackList(self):
        return self.__attackList

    def getPreviousAttack(self):
        return self.__previousAttack

    def getXpValue(self):
        return self.__XpValue

    def getCheeseCounter(self):
        return self.__cheeseCounter

    def getShieldStatus(self):
        return self.__shieldStatus

    def getMaxMana(self):
        return self.__maxMana

    def getCurrentMana(self):
        return self.__currentMana

    def getBossManaBar(self):
        return self.__boss_mana_bar

    def getBoss(self):
        return self.__boss


    #mutators
    def setAttackList(self, newAttackList):
        self.__attackList = newAttackList

    def setPreviousAttack(self, newPreviousAttack):
        self.__previousAttack = newPreviousAttack

    def setXpValue(self, newXpValue):
        self.__XpValue = newXpValue

    def setCheeseCounter(self, newCheeseCounter):
        self.__cheeseCounter = newCheeseCounter

    def setShieldStatus(self, newShieldStatus):
        self.__shieldStatus = newShieldStatus

    def setMaxMana(self, newMaxMana):
        self.__maxMana = newMaxMana

    def setCurrentMana(self, newCurrentMana):
        self.__currentMana = newCurrentMana

    def setBossManaBar(self, newBossmanabar):
        self.__boss_mana_bar = newBossmanabar

    def setBoss(self, newBoss):
        self.__boss = newBoss


    # behaviours
    def move(self): # Boss doesn't need to move (cool sunglasses emoji)
        pass

    def attack(self, target):
        output = []
        attackRNG = random.randint(1,100)

        # Boss Attack pattern logic
        if not self.__shieldStatus[0] and attackRNG <90: # Add some chance just for the fun of it
            selected_attack = "Magic Shield"
        elif self.getCurrentHP() < self.getMaxHP()/2 and attackRNG <= 80:
            selected_attack = "Unfair turn cheat"
        elif self.getCurrentMana() < self.getMaxMana()/2 and attackRNG <= 20:
            selected_attack = "Unfair mana cheat"
        elif self.getCurrentHP() == 1 and self.__previousAttack != "Unfair turn cheat" and self.__previousAttack != "Magic Shield": # Don't make the heal rng based
            selected_attack = "Unfair HP cheat"
        elif attackRNG < 50:
            selected_attack = "Magic Nuclear Arsenal"
        else:
            selected_attack = "Conjure Cheese"
        

        attack_output = self.__attackList[selected_attack](target)
        self.__previousAttack = selected_attack
        return attack_output

    # attacks
    def magic_shield(self, player):
        output = []
        turns = 3
        self.__shieldStatus = True, turns
        output.append(f"{self.getName()} creates a really cool magical barrier that blocks 90% of incoming damage lasing {turns} turns.")
        
        return output

    def turn_cheat(self, player):
        output = []
        output.append(f"{self.getName()} casts an Unfair Turn Cheat with his dark magic, cheating in 2 turns")
        bonus_turns=2
        while bonus_turns>0: # Attacks until the bonus turns are used up
            output.append(self.attack(player))
        return output

    def mana_cheat(self, player):
        output = []
        output.append(f"{self.getName()} casts an Unfair Mana Cheat with his dark magic, cheating his mana to full")
        self.setCurrentMana(self.getMaxMana())
        return output
    
    def HP_cheat(self, player):
        output = []
        output.append(f"{self.getName()} casts an Unfair HP Cheat with his dark magic, cheating his HP to full")
        self.setCurrentHP(self.getMaxHP())
        return output
    
    def magic_nuclear_arsenal(self, player):
        output = []
        damage = (self.getMagicPower() + 50) * player.getMagicResistance()
        output.append(f"{self.getName()} slams {player.getName()} with what is effectively a magical equivilent of the USA's nuclear arsenal.")
        damage_output = player.takeDamage(damage)
        output.extend(damage_output)
        return output
    
    def conjure_cheese(self, player):
        output = []
        output.append(f"{self.getName()} conjures an appetizing wheel of cheese...")
        self.__cheeseCounter += 1
        output.append(f"{self.getName()} now has {self.__cheeseCounter} cheese wheels in his presence.")

        if self.__cheeseCounter >= 3 and self.getCurrentHP() <= self.getMaxHP()/2 + 10*self.__cheeseCounter:
            output.append(f"The cheese wheels unite in the dreams and aspirations of {self.getName()}, manifesting the true form of The Cheese God itself.")
            damage = 999999999999999
            output.append(f"You look ready for a fight but The Cheese God is too overwhelming in its power, its mere presence erasing your very existence with {damage} damage.")

        return output

    # Game features
    
    def takeDamage(self, damage):
        output = []
        if self.__shieldStatus[0]:
            damage = damage * 0.1
            output.append(f"Magic shield blocked 90% of incoming damage, reducing damage to {damage}.")
            if self.getCurrentHP() - damage <= 0 and self.getCurrentHP() > 1: # Check for fatal damage and whether the last attack also cheated fatal damage
                self.setCurrentHP(damage + 1) # Makes sure the boss survives a fatal hit if the conditions are met
                output.append(f"Since the incoming damage was still fatal, {self.getName()} had to rely on the magic barrier to cheat death.")
            output.append

        self.setCurrentHP(self.getCurrentHP() - damage)
        output.append(f"{self.getName()} has {self.getCurrentHP()} HP remaining")
        return output
    
    def upkeepPhase(self): # Gets an upkeep since its a boss
        output = ["End of enemy turn: "]

        self.setCurrentMana(min(self.__maxMana, self.__currentMana + 20))
        output.append(f"{self.getName()} has regenerated 20 mana. (not that he needed it)")
        
        if self.__shieldStatus[1] == 0:
            self.__shieldStatus = False, None  # stops being exposed upon next turn
            output.append(f"{self.getName()} is no longer shielded!")
        elif self.__shieldStatus[1]:
            self.__shieldStatus = True, self.__shieldStatus[1] - 1
            output.append(f"{self.getName()}'s shield falters in {self.__shieldStatus[1]} turns.")


        return output


    def draw(self, newPosition, size):
        ''' Draw the skeleton image on the window at the current position'''

        # Generate a random position if this class has no position currently 
        if not self.getPosition():
            startingX = random.randint(100, self.getWindow().get_width() - 100)
            startingY = random.randint(100, self.getWindow().get_height() - 100)
            self.setPosition((startingX, startingY))

        if newPosition: # check if a different position is specified for the skeleton to be drawn at
            position = newPosition # use the new position instead.
        else:
            position = self.getPosition() # if no new position is given, it uses its current position instead

        image = pygame.transform.scale(self.getImage(), (size)) # Resizes the image to be drawn based on the given dimensions

        self.getWindow().blit(image, position)
