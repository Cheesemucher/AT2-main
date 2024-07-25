from abc import ABC, abstractmethod
from bar import Bar
from skill_point_distributor import SkillPointsAllocator

class Character:
    #attributes
    MAX_LEVEL = 50  # Maximum level a character can reach
    ATTRIBUTE_POINTS_PER_LEVEL = 3  # Number of attribute points gained per level
    __name = None  # Character's name
    __maxHP = None
    __currentHP = None
    __character_class = None  # Character's class
    __defenseMultiplier = None  # decimal multiplier representing % of physical damage that will be dealt upon getting hit
    #not called defense because it is the damage that you DO take, not damage blocked
    __magicResistance = None # decimal multiplier representing % of magic damage recieved upon hit
    __exposed = None # status effect that increases incoming damage
    __level = None  # Character's current level
    __EXP = None  # Character's current experience points
    __EXP_to_next_level = None  # How much xp you need to get to the next level
    __attribute_points = None  # Attribute points available to allocate
    __cursedStatus = None
    __curseTimer = None # no. of turns that a curse needs to deal the damage
    __skillPointDistributor = None
    __player_health_bar = None
    __player_resource_bar = None
    
    #end attributes

    #constructors
    def __init__(self, name, characterclass, armor, magicResistance, window):
        self.__name = name
        self.__level = 1
        self.__EXP = 0
        self.__character_class = characterclass
        self.__defenseMultiplier = armor/100
        self.__magicResistance = magicResistance/100
        self.__exposed = (False, None)
        self.__maxHP = 100 + (self.__level * 20)
        self.__currentHP = self.__maxHP
        self.__EXP_to_next_level = 100
        self.__attribute_points = 0
        self.__cursedStatus = {"status":None, #boolean cursed state flag
                               "delay":None,  #turn count for timer to reach
                               "damage":None} #damage taken when timer is reached
        self.__curseTimer = 0
        self.__skillPointDistributor = SkillPointsAllocator(self)

    #accessors
    def getMAXLEVEL(self):
        return self.MAX_LEVEL

    def getATTRIBUTEPOINTSPERLEVEL(self):
        return self.ATTRIBUTE_POINTS_PER_LEVEL

    def getName(self):
        return self.__name

    def getMaxHP(self):
        return self.__maxHP

    def getCurrentHP(self):
        return self.__currentHP

    def getCharacterclass(self):
        return self.__character_class

    def getDefenseMultiplier(self):
        return self.__defenseMultiplier

    def getMagicResistance(self):
        return self.__magicResistance

    def getExposedStatus(self):
        return self.__exposed

    def getLevel(self):
        return self.__level

    def getEXP(self):
        return self.__EXP

    def getEXPtonextlevel(self):
        return self.__EXP_to_next_level

    def getAttributepoints(self):
        return self.__attribute_points

    def getCursedStatus(self):
        return self.__cursedStatus

    def getCurseTimer(self):
        return self.__curseTimer
    
    def getSkillPointDistributor(self):
        return self.__skillPointDistributor

    #mutators
    def setMAXLEVEL(self, newMAXLEVEL):
        self.MAX_LEVEL = newMAXLEVEL

    def setATTRIBUTEPOINTSPERLEVEL(self, newATTRIBUTEPOINTSPERLEVEL):
        self.ATTRIBUTE_POINTS_PER_LEVEL = newATTRIBUTEPOINTSPERLEVEL

    def setName(self, newName):
        self.__name = newName

    def setMaxHP(self, newMaxHP):
        self.__maxHP = newMaxHP

    def setCurrentHP(self, newCurrentHP):
        self.__currentHP = newCurrentHP

    def setCharacterclass(self, newCharacterclass):
        self.__character_class = newCharacterclass

    def setDefenseMultiplier(self, newDefenseMultiplier):
        self.__defenseMultiplier = newDefenseMultiplier

    def setMagicResistance(self, newMagicResistance):
        self.__magicResistance = newMagicResistance

    def setExposedStatus(self, newExposedStatus, duration):
        self.__exposed = (newExposedStatus, duration)

    def setLevel(self, newLevel):
        self.__level = newLevel

    def setEXP(self, newEXP):
        self.__EXP = newEXP

    def setEXPtonextlevel(self, newEXPtonextlevel):
        self.__EXP_to_next_level = newEXPtonextlevel

    def setAttributepoints(self, newAttributepoints):
        self.__attribute_points = newAttributepoints

    def setCursedStatus(self, status, delay, damage):
        self.__cursedStatus["damage"] = damage
        self.__cursedStatus["delay"] = delay
        self.__cursedStatus["status"] = status

    def setCurseTimer(self, newTimer):
        self.__curseTimer = newTimer

    def setSkillPointDistributor(self, newDistributor):
        self.__curseTimer = newDistributor

    #behaviours
    def gain_experience(self, experience):
        self.__EXP += experience  # Increase character's experience points

        while self.leveled_up() and self.__level < self.MAX_LEVEL: # While loop to allow double level ups
            print(f"Level up! {self.__name} is now level {self.__level}.")
            
            self.__level += 1  # Level up the character
            self.__EXP -= self.__EXP_to_next_level  # Decrease character's experience points
            self.__attribute_points += self.ATTRIBUTE_POINTS_PER_LEVEL  # grant attribute points

            # Calculate experience required for next level
            self.__EXP_to_next_level = self.calculate_required_experience(self.__level + 1)
        
        if self.__attribute_points:
            return self.__skillPointDistributor.distribute_points(self, self.__attribute_points)
        
        else: 
            return self

    def leveled_up(self):
        return self.__EXP >= self.__EXP_to_next_level

    def calculate_required_experience(self, level):
        # Example exponential scaling: Each level requires 100 more experience points than the previous level
        return int(100 * (1.5 ** (level - 1)))

    def isAlive(self):
        return self.getCurrentHP() > 0

    @abstractmethod 
    def takeDamage(self, amount):
        pass

    @abstractmethod
    def upkeepPhase(self):
        pass


