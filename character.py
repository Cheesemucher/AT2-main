class Character:
    #attributes
    MAX_LEVEL = 50  # Maximum level a character can reach
    ATTRIBUTE_POINTS_PER_LEVEL = 3  # Number of attribute points gained per level
    __name = None  # Character's name
    __character_class = None  # Character's class
    __armor = None  # % of physical damage that will be dealt upon getting hit
    __magicResistance = None # % of magic damage recieved upon hit
    __level = 1  # Character's current level
    __experience_points = 0  # Character's current experience points
    __hit_points = 10  # Example starting value for character's hit points
    __skills = {}  # Example empty dictionary for character's skills
    __inventory = []  # Example empty list for character's inventory
    __gold = 0  # Example starting value for character's gold
    __attribute_points = 0  # Attribute points available to allocate
    #end attributes

    #constructors
    def __init__(self, name, characterclass, armor, magicResistance):
        self.__name = name
        self.__character_class = characterclass
        self.__armor = armor
        self.__magicResistance = magicResistance

    #accessors
    def getMAXLEVEL(self):
        return self.__MAX_LEVEL

    def getATTRIBUTEPOINTSPERLEVEL(self):
        return self.__ATTRIBUTE_POINTS_PER_LEVEL

    def getName(self):
        return self.__name

    def getCharacterclass(self):
        return self.__character_class

    def getArmor(self):
        return self.__armor

    def getLevel(self):
        return self.__level

    def getExperiencepoints(self):
        return self.__experience_points

    def getHitpoints(self):
        return self.__hit_points

    def getArmorclass(self):
        return self.__armor_class

    def getSkills(self):
        return self.__skills

    def getInventory(self):
        return self.__inventory

    def getGold(self):
        return self.__gold

    def getAttributepoints(self):
        return self.__attribute_points
    
    def getMagicResistance(self):
        return self.__magicResistance

    #mutators
    def setMAXLEVEL(self, newMAXLEVEL):
        self.__MAX_LEVEL = newMAXLEVEL

    def setATTRIBUTEPOINTSPERLEVEL(self, newATTRIBUTEPOINTSPERLEVEL):
        self.__ATTRIBUTE_POINTS_PER_LEVEL = newATTRIBUTEPOINTSPERLEVEL

    def setName(self, newName):
        self.__name = newName

    def setCharacterclass(self, newCharacterclass):
        self.__character_class = newCharacterclass

    def setArmor(self, newArmor):
        self.__armor = newArmor

    def setLevel(self, newLevel):
        self.__level = newLevel

    def setExperiencepoints(self, newExperiencepoints):
        self.__experience_points = newExperiencepoints

    def setHitpoints(self, newHitpoints):
        self.__hit_points = newHitpoints

    def setMagicResistance(self, newMR):
        self.__magicResistance = newMR

    def setSkills(self, newSkills):
        self.__skills = newSkills

    def setInventory(self, newInventory):
        self.__inventory = newInventory

    def setGold(self, newGold):
        self.__gold = newGold

    def setAttributepoints(self, newAttributepoints):
        self.__attribute_points = newAttributepoints

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

    def is_alive(self):
        return self.__hit_points > 0

    def take_damage(self, amount):
        # Calculate the actual damage taken, taking into account the character's armor
        actual_damage = max(0, amount - self.__armor)
        self.__hit_points -= actual_damage
        if self.__hit_points <= 0:
            print(f"{self.__name} takes {actual_damage} damage and has been defeated!")
        else:
            print(f"{self.__name} takes {actual_damage} damage. Remaining hit points: {self.__hit_points}")
