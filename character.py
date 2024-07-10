from abc import ABC, abstractmethod

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
    __exposed = None
    __level = None  # Character's current level
    __EXP = None  # Character's current experience points
    __skills = {}  # Example empty dictionary for character's skills
    __inventory = []  # Example empty list for character's inventory
    __gold = None  # Example starting value for character's gold
    __attribute_points = None  # Attribute points available to allocate
    __cursedStatus = None
    __curseTimer = None # no. of turns that a curse needs to deal the damage
    #end attributes

    #constructors
    def __init__(self, name, characterclass, armor, magicResistance):
        self.__name = name
        self.__level = 1
        self.__EXP = 0
        self.__character_class = characterclass
        self.__defenseMultiplier = armor/100
        self.__magicResistance = magicResistance/100
        self.__exposed = False
        self.__maxHP = 100 + (self.__level * 20)
        self.__currentHP = self.__maxHP
        self.__gold = 0
        self.__attribute_points = 0
        self.__cursedStatus = {"status":None, #boolean cursed state flag
                               "delay":None,  #turn count for timer to reach
                               "damage":None} #damage taken when timer is reached
        self.__curseTimer = 0

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

    def getLevel(self):
        return self.__level

    def getEXP(self):
        return self.__EXP

    def getSkills(self):
        return self.__skills

    def getInventory(self):
        return self.__inventory

    def getGold(self):
        return self.__gold

    def getAttributepoints(self):
        return self.__attribute_points
    
    def getExposedStatus(self):
        return self.__exposed
    
    def getCursedStatus(self):
        return self.__cursedStatus
    
    def getCursedTimer(self):
        return self.__curseTimer


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

    def setLevel(self, newLevel):
        self.__level = newLevel

    def setEXP(self, newEXP):
        self.__EXP = newEXP

    def setSkills(self, newSkills):
        self.__skills = newSkills

    def setInventory(self, newInventory):
        self.__inventory = newInventory

    def setGold(self, newGold):
        self.__gold = newGold

    def setAttributepoints(self, newAttributepoints):
        self.__attribute_points = newAttributepoints

    def setExposedStatus(self, newExposedStatus):
        self.__exposed = newExposedStatus

    def setCursedStatus(self, status, delay, damage):
        self.__cursedStatus["damage"] = damage
        self.__cursedStatus["delay"] = delay
        self.__cursedStatus["status"] = status

    def setCursedTimer(self, newTimer):
        self.__curseTimer = newTimer

    #behaviours
    def assign_attribute_points(self, attribute, points):
        # Ensure the attribute exists before assigning points
        private_attribute = f"__{attribute}"
        if private_attribute in self.__dict__:
            setattr(self, private_attribute, getattr(self, private_attribute) + points)  # Add points to the attribute
            self.__attribute_points -= points  # Decrease available attribute points
        else:
            print(f"Error: Attribute '{attribute}' does not exist.")

    def gain_experience(self, experience):
        self.__experience_points += experience  # Increase character's experience points
        # Calculate experience required for next level
        required_experience = self.calculate_required_experience(self.__level + 1)
        # Check if character has enough experience to level up and is below the level cap
        while self.__experience_points >= required_experience and self.__level < self.__MAX_LEVEL:
            self.__level += 1  # Level up the character
            self.__experience_points -= required_experience  # Decrease character's experience points
            self.__hit_points += 10  # Example: Increase hit points by 10 each level up
            self.__attribute_points += self.__ATTRIBUTE_POINTS_PER_LEVEL  # Allocate attribute points
            print(f"Level up! {self.__name} is now level {self.__level}.")
            # Calculate experience required for next level
            required_experience = self.calculate_required_experience(self.__level + 1)

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


