from character import Character
from textWriter import TextRenderer
from bar import Bar
import random

class Ninja(Character):
    # attributes
    __maxStamina = None
    __currentStamina = None
    __staminaRegeneration = None
    __strength = None
    __dodgeChance = None
    __critChance = None
    __concealed = None
    __attacks = None
    __stats = None
    # end attributes

    def __init__(self, name, window):
        super().__init__(name, "Ninja", 90, 100, window)
        self.__maxStamina = 100
        self.__currentStamina = self.__maxStamina
        self.__staminaRegeneration = 20
        self.__strength = 45
        self.__dodgeChance = 30  # % chance to dodge attacks
        self.__critChance = 20  # % chance to crit
        self.__concealed = False
        self.__player_health_bar = Bar(window, self, (10,10), "HP") # Make a bar object to track players health
        self.__player_resource_bar = Bar(window, self, (10,40), "Stamina") # Make a bar object to track players stamina/mana
        self.__attacks = {
            "Shuriken Throw": {"method": self.shurikenThrow, "staminaCost": 10},
            "Ninjago": {"method": self.Ninjago, "staminaCost": 30},
            "Epic Katana Enemy Dicer Move": {"method": self.katana, "staminaCost": 40},
            "Smoke Bomb": {"method": self.smokeBomb, "staminaCost": 30},
            "Ninja Concentration": {"method": self.ninjaConcentration, "staminaCost": 0},
        }
        self.__stats = {
            "Stamina Regen Rate": self.getStaminaRegeneration(),
            "Strength":self.getStrength(),
            "Max Stamina":self.getMaxStamina(),
            "Current Stamina": self.getCurrentStamina(),
            "Max HP":self.getMaxHP(),
            "Current HP": self.getCurrentHP(),
            "Defense Multiplier": self.getDefenseMultiplier(),
            "Magic Resistance Multiplier": self.getMagicResistance(),
            "Dodge Chance": self.getDodgeChance(),
        }

    # accessors
    def getMaxStamina(self):
        return self.__maxStamina 

    def getCurrentStamina(self):
        return self.__currentStamina

    def getStaminaRegeneration(self):
        return self.__staminaRegeneration + (2 * self.getLevel())
    
    def getStrength(self):
        return self.__strength

    def getDodgeChance(self):
        return self.__dodgeChance

    def getCritChance(self):
        return self.__critChance

    def getConcealedStatus(self):
        return self.__concealed
    
    def getStats(self):
        self.__stats = {
            "Stamina Regen Rate": self.getStaminaRegeneration(),
            "Strength":self.getStrength(),
            "Max Stamina":self.getMaxStamina(),
            "Current Stamina": self.getCurrentStamina(),
            "Max HP":self.getMaxHP(),
            "Current HP": self.getCurrentHP(),
            "Defense Multiplier": self.getDefenseMultiplier(),
            "Magic Resistance Multiplier": self.getMagicResistance(),
            "Dodge Chance": self.getDodgeChance(),
        }

        return self.__stats
    
    def getPlayerHealthBar(self):
        return self.__player_health_bar

    def getPlayerResourceBar(self):
        return self.__player_resource_bar

    # mutators
    def setMaxStamina(self, newMaxStamina):
        self.__maxStamina = newMaxStamina

    def setCurrentStamina(self, newCurrentStamina):
        self.__currentStamina = newCurrentStamina

    def setStaminaRegeneration(self, newStaminaRegeneration):
        self.__staminaRegeneration = newStaminaRegeneration

    def setStrength(self, newStrength):
        self.__strength = newStrength

    def setDodgeChance(self, newDodgeChance):
        self.__dodgeChance = newDodgeChance
        if self.__dodgeChance >= 100:
            self.__dodgeChance = 99
            return (f"{self.getName()} was unable to reach the omniscient potential required to reach 100% dodge chance.")

    def setCritChance(self, newCritChance):
        self.__critChance = newCritChance

    def setConcealedStatus(self, newConcealedStatus):
        self.__concealed = newConcealedStatus

    def setStats(self, newStats):
        self.__stats = newStats

    def setPlayerHealthBar(self, healthBar):
        self.__player_health_bar = healthBar

    def setPlayerResourceBar(self, resourceBar):
        self.__player_resource_bar = resourceBar

    # behaviours
    def listAttacks(self, window, attackMenuArea, fontSize):
        attack_writer = TextRenderer(window, attackMenuArea, fontSize) 

        attack_list = ["Attack List:"]
        
        attackList = list(self.__attacks.items())
        for i, (attack, info) in enumerate(attackList): # Displays all attack info within the space outlined in the parameters
            attack_list.append(f"{i + 1}. {attack} (Stamina cost: {info['staminaCost']})")
        
        attack_writer.display_output(attack_list)

    def attack(self, target, chosen_attack):
        output = []
        
        attackList = list(self.__attacks.items())
        if 1 <= chosen_attack <= len(attackList):
            attack, attackInfo = attackList[chosen_attack - 1]
            if self.getCurrentStamina() >= attackInfo["staminaCost"]:
                remainingStamina = self.getCurrentStamina() - attackInfo["staminaCost"]
                self.setCurrentStamina(remainingStamina)
                attackMethod = attackInfo["method"]
                attackOutput = attackMethod(target)
                output.extend(attackOutput)
            else:
                output.append(f"{self.getName()} got ready for a move, but collapsed from exhaustion instead.")
        else:
            output.append("Invalid attack.")

        self.getPlayerResourceBar().update_quantity() # Update the stamina/mana bar      

        return output

    def attackDodged(self):
        DodgeRNG = random.randint(1, 100)
        return DodgeRNG <= self.getDodgeChance()

    def criticalStrike(self):
        CritRNG = random.randint(1, 100)
        return CritRNG <= self.getCritChance()

    def shurikenThrow(self, target):
        output = []
        if self.criticalStrike():
            damage = self.getStrength() * target.getDefenseMultiplier() + (self.getStrength() / 2)
            output.append(f"{self.getName()} launches a shuriken at {target.getName()}'s weakest area for {damage} damage!")
        else:
            damage = self.getStrength() * target.getDefenseMultiplier()
            output.append(f"{self.getName()} launches a shuriken at {target.getName()} for {damage} damage!")
        damage_output = target.takeDamage(damage)
        output.extend(damage_output)
        return output

    def Ninjago(self, target):
        output = []
        damage = self.getStrength() * target.getDefenseMultiplier() + 20  # the +20 is the stamina cost
        output.append(f"NINJAGO! ({damage} damage)")
        damage_output = target.takeDamage(damage)
        output.extend(damage_output)
        return output

    def katana(self, target):
        output = []
        damage = self.getStrength() * target.getDefenseMultiplier() * 2
        damage += damage * (target.getMaxHP() - target.getCurrentHP()) / target.getMaxHP()  # adds damage based on % of enemy health missing
        output.append(f"{self.getName()} dices {target.getName()} in a badass series of epic katana slices. for {damage} damage.")
        damage_output = target.takeDamage(damage)
        output.extend(damage_output)
        return output

    def smokeBomb(self, target):
        output = []

        output.append(f"{self.getName()}'s reflexes are heightened and dodge chance is now {self.getDodgeChance()}%.")
        dodge_message = self.setDodgeChance(self.getDodgeChance() + 5)
        if dodge_message:
            output.append(dodge_message)

        if self.attackDodged() or self.getDodgeChance() > 30:
            self.setConcealedStatus(2)
            output.append(f"{self.getName()} vanishes within a cloud of smoke, like a true badass ninja.")
        else:
            output.append(f"{self.getName()}'s smoke bomb threw out a cloud of smoke, but {self.getName()} was not stealthy enough to hide in it and enters a coughing fit.")
        return output

    def ninjaConcentration(self, target):
        output = []

        output.append(f"{self.getName()} focuses on the balance of the universe, able to now hear the wing beat of a butterfly. {self.getName()}'s dodge chance is now {self.getDodgeChance()}% for the rest of the battle")
        dodge_message = self.setDodgeChance(self.getDodgeChance() + 10)
        if dodge_message:
            output.append(dodge_message)
        
        return output

    # turn based combat related behaviours
    def takeDamage(self, amount):
        output = []
        if self.getConcealedStatus():
            output.append(f"{self.getName()} could not be found in the cloud of smoke, leaving no enemy to hit.")
        elif self.attackDodged():
            output.append(f"{self.getName()}'s quick ninja reflexes and agility allow him to completely avoid all damage!")
        elif self.getExposedStatus()[0]: # Being unseen is mutually exclusive with exposed status effects
            output.append(f"{self.getName()}'s exposed state rendered all armor ineffective.")
            amount = amount / self.getDefenseMultiplier()
        else:
            self.setCurrentHP(self.getCurrentHP() - amount)
            output.append(f"{self.getName()} takes {amount} damage.")
        output.append(f"{self.getName()} has {self.getCurrentHP()} HP remaining")
        
        self.getPlayerHealthBar().update_quantity() # Update the health bar to show new HP
        return output

    def upkeepPhase(self):
        output = ["End of turn: "]
        self.setCurrentStamina(min(self.__maxStamina, self.__currentStamina + self.__staminaRegeneration)) # Regen some stamina
        output.append(f"{self.getName()} has regenerated {self.__staminaRegeneration} stamina.")
        self.__player_resource_bar.update_quantity()
        
        if self.getExposedStatus()[1] == 0:
            self.setExposedStatus(False, None)  # stops being exposed upon next turn
            output.append(f"{self.getName()} is no longer exposed!")
        elif self.getExposedStatus()[1]:
            self.setExposedStatus(True, self.getExposedStatus()[1] - 1)
            output.append(f"{self.getName()} remains exposed for another {self.getExposedStatus()[1]} turns.")

        if self.getConcealedStatus() >0:
            self.setConcealedStatus(self.getConcealedStatus()-1)
        else:
            output.append(f"The smoke cloud dissipates, leaving {self.getName()} in the open again.")

        if self.getCursedStatus()["status"]:
            self.setCurseTimer(self.getCurseTimer() + 1)
            if self.getCurseTimer() >= self.getCursedStatus()["delay"]:
                damage = self.getCursedStatus()["damage"]

                self.setCurrentHP(self.getCurrentHP() - damage)
                output.append(f"The curse has taken hold. {self.getName()} has suffered {damage} damage!")
                self.setCurseTimer(0)
                self.setCursedStatus(False, None, None)

                output.append(f"{self.getName()} has {self.getCurrentHP()} HP remaining")
            else:
                turnsLeft = self.getCursedStatus()["delay"] - self.getCurseTimer()
                output.append(f"The curse manifests in {turnsLeft} more turn(s)...")

        return output

    def battle_end(self):
        self.setCursedStatus(False, None, None)
        self.setDodgeChance(self.getDodgeChance/2 - 10)