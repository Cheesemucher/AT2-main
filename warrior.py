from character import Character
from textWriter import TextRenderer

class Warrior(Character):
    # Attributes
    __maxStamina = None
    __currentStamina = None
    __staminaRegeneration = None
    __strength = None
    __defensiveStance = None

    __attacks = None

    def __init__(self, name):
        super().__init__(name, "Warrior", 60, 80)
        self.__maxStamina = 100
        self.__currentStamina = self.__maxStamina
        self.__staminaRegeneration = 10
        self.__strength = 50
        self.__defensiveStance = False
        self.__attacks = {
            "Slash": {"method": self.slash, "staminaCost": 10},
            "Lunge": {"method": self.lunge, "staminaCost": 20},
            "Cleave": {"method": self.cleave, "staminaCost": 30},
            "Shield Bash": {"method": self.shieldBash, "staminaCost": 15},
            "Defensive Stance": {"method": self.defensiveStance, "staminaCost": 5},
        }

    # Accessors
    def getMaxStamina(self):
        return self.__maxStamina

    def getCurrentStamina(self):
        return self.__currentStamina

    def getStaminaRegeneration(self):
        return self.__staminaRegeneration

    def getStrength(self):
        return self.__strength

    def getDefensiveStance(self):
        return self.__defensiveStance

    def getAttacks(self):
        return self.__attacks

    # Mutators
    def setMaxStamina(self, maxStamina):
        self.__maxStamina = maxStamina

    def setCurrentStamina(self, currentStamina):
        self.__currentStamina = currentStamina

    def setStaminaRegeneration(self, staminaRegeneration):
        self.__staminaRegeneration = staminaRegeneration

    def setStrength(self, strength):
        self.__strength = strength

    def setDefensiveStance(self, defensiveStanceStatus):
        self.__defensiveStance = defensiveStanceStatus

    def setAttacks(self, attacks):
        self.__attacks = attacks

    # behaviors
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

        return output #used the output to be returned here instead of returning the single events as a list is expected by the textWriter class anyway

    def lunge(self, target):
        output = []

        damage = self.getStrength() * 1.8 * target.getDefenseMultiplier()
        output.append(f"{self.getName()} lunges at {target.getName()} for {damage} damage!")
        damage_output = target.takeDamage(damage)
        output.extend(damage_output)

        output.append(f"{self.getName()}'s lunge has left him exposed.")
        self.setExposedStatus(True)

        return output

    def slash(self, target):
        output = []

        damage = self.getStrength() * target.getDefenseMultiplier()
        output.append(f"{self.getName()} slashes at {target.getName()} for {damage} damage!")
        damage_output = target.takeDamage(damage)
        output.extend(damage_output)

        return output

    def cleave(self, target):
        output = []

        damage = self.getStrength() + 10 * target.getDefenseMultiplier()
        output.append(f"{self.getName()} dealt a total of {damage} damage with cleave!")
        damage_output = target.takeDamage(damage)
        output.extend(damage_output)

        return output

    def shieldBash(self, target):
        output = []

        if self.getDefensiveStance():
            output.append(f"{self.getName()}'s defensive stance enabled a more forceful shield bash!")
            damage = (self.getStrength() + 100 - 100 * self.getDefenseMultiplier()) * target.getDefenseMultiplier()
        else:
            damage = self.getStrength() * target.getDefenseMultiplier()

        output.append(f"{self.getName()} shield bashes {target.getName()} for {damage} damage!")
        damage_output = target.takeDamage(damage)
        output.extend(damage_output)

        return output

    def defensiveStance(self, target):
        output = []

        self.setDefensiveStance(True)
        output.append(f"{self.getName()} takes a defensive stance, reducing incoming physical damage.")
        damage = target.getDefenseMultiplier() * 5
        output.append(f"{target.getName()} is intimidated and takes {damage} damage!")
        damage_output = target.takeDamage(damage)
        output.extend(damage_output)

        return output

    # Turn-based combat related behaviors
    def takeDamage(self, amount):
        output = []

        if self.getDefensiveStance():
            amount = max(amount - (100 - 100 * self.getDefenseMultiplier()), 0)
            output.append(f"{self.getName()}'s defensive stance further reduced incoming damage to a total of {amount}!")

        if self.getExposedStatus():
            output.append(f"{self.getName()}'s exposed state rendered all armor ineffective.")
            amount = amount / self.getDefenseMultiplier()

        self.setCurrentHP(self.getCurrentHP() - amount)
        output.append(f"{self.getName()} has {self.getCurrentHP()} HP remaining")

        return output

    def upkeepPhase(self):
        self.setCurrentStamina(min(self.__maxStamina, self.__currentStamina + self.__staminaRegeneration))
        self.setExposedStatus(False)

        output = []
        if self.getCursedStatus()["status"]:
            self.setCursedTimer(self.getCursedTimer() + 1)
            if self.getCursedTimer() >= self.getCursedStatus()["delay"]:
                damage = self.getCursedStatus()["damage"]

                self.setCurrentHP(self.getCurrentHP() - damage)
                output.append(f"The curse has taken hold. {self.getName()} has suffered {damage} damage!")
                self.setCursedTimer(0)
                self.setCursedStatus(False, None, None)

                output.append(f"{self.getName()} has {self.getCurrentHP()} HP remaining")
            else:
                turnsLeft = self.getCursedStatus()["delay"] - self.getCursedTimer()
                output.append(f"The curse manifests in {turnsLeft} more turn(s)...")

        return output
