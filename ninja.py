from character import Character
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
    # end attributes

    def __init__(self, name):
        super().__init__(name, "Ninja", 90, 100)
        self.__maxStamina = 100 + (2 * self.getLevel())
        self.__currentStamina = self.__maxStamina
        self.__staminaRegeneration = 10
        self.__strength = 45
        self.__dodgeChance = 30  # % chance to dodge attacks
        self.__critChance = 20  # % chance to crit
        self.__concealed = False
        self.__attacks = {
            "Shuriken Throw": {"method": self.shurikenThrow, "staminaCost": 10},
            "Ninjago": {"method": self.Ninjago, "staminaCost": 30},
            "Epic Katana Enemy Dicer Move": {"method": self.katana, "staminaCost": 40},
            "Smoke Bomb": {"method": self.smokeBomb, "staminaCost": 30},
            "Ninja Concentration": {"method": self.ninjaConcentration, "staminaCost": 0},
        }

    # accessors
    def getMaxStamina(self):
        return self.__maxStamina

    def getCurrentStamina(self):
        return self.__currentStamina

    def getStaminaRegeneration(self):
        return self.__staminaRegeneration

    def getStrength(self):
        return self.__strength

    def getDodgeChance(self):
        return self.__dodgeChance

    def getCritChance(self):
        return self.__critChance

    def getConcealedStatus(self):
        return self.__concealed

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
            print(f"{self.getName()} was unable to reach the omniscient potential required to reach 100% dodge chance.")

    def setCritChance(self, newCritChance):
        self.__critChance = newCritChance

    def setConcealedStatus(self, newConcealedStatus):
        self.__concealed = newConcealedStatus

    # behaviours
    def chooseAttack(self, target):
        output = []
        print(f"Choose an attack (Current stamina: {self.__currentStamina}):")
        attackList = list(self.__attacks.items())
        for i, (attack, info) in enumerate(attackList):
            print(f"{i + 1}. {attack} (Stamina cost: {info['staminaCost']})")
        chosenAttack = int(input("Enter the number of the attack: "))
        if 1 <= chosenAttack <= len(attackList):
            attack, attackInfo = attackList[chosenAttack - 1]
            if self.getCurrentStamina() >= attackInfo["staminaCost"]:
                remainingStamina = self.getCurrentStamina() - attackInfo["staminaCost"]
                self.setCurrentStamina(remainingStamina)
                attackMethod = attackInfo["method"]
                attackOutput = attackMethod(target)
                output.extend(attackOutput)
            else:
                output.append(f"{self.getName()} prepared for the attack, but collapsed from exhaustion instead.")
        else:
            output.append("Invalid attack.")
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
        output.append(f"{self.getName()} dices {target.getName()} in a badass series of epic katana slices.")
        damage_output = target.takeDamage(damage)
        output.extend(damage_output)
        return output

    def smokeBomb(self, target):
        output = []
        self.setDodgeChance(self.getDodgeChance() + 5)
        output.append(f"{self.getName()}'s reflexes are heightened and dodge chance is now {self.getDodgeChance()}%.")

        if self.attackDodged() or self.getDodgeChance() > 30:
            self.setConcealedStatus(True)
            output.append(f"{self.getName()} vanishes within a cloud of smoke, like a true badass ninja.")
        else:
            output.append(f"{self.getName()}'s smoke bomb threw out a cloud of smoke, but {self.getName()} was not stealthy enough to hide in it and enters a coughing fit.")
        return output

    def ninjaConcentration(self, target):
        output = []
        self.setDodgeChance(self.getDodgeChance() + 10)
        output.append(f"{self.getName()} focuses on the balance of the universe, able to now hear the wing beat of a butterfly. {self.getName()}'s dodge chance is now {self.getDodgeChance()}% for the rest of the battle")
        return output

    # turn based combat related behaviours
    def takeDamage(self, amount):
        output = []
        if self.getConcealedStatus():
            output.append(f"{self.getName()} could not be found in the cloud of smoke, leaving no enemy to hit.")
        elif self.attackDodged():
            output.append(f"{self.getName()}'s quick ninja reflexes and agility allow him to completely avoid all damage!")
        else:
            self.setCurrentHP(self.getCurrentHP() - amount)
            output.append(f"{self.getName()} takes {amount} damage.")
        output.append(f"{self.getName()} has {self.getCurrentHP()} HP remaining")
        return output

    def upkeepPhase(self):
        output = []
        self.setCurrentStamina(min(self.__maxStamina, self.__currentStamina + self.__staminaRegeneration))
        self.setExposedStatus(False)  # stops being exposed upon next turn
        if self.getConcealedStatus():
            output.append(f"The smoke cloud dissipates, leaving {self.getName()} in the open again.")
            self.setConcealedStatus(False)
        return output
