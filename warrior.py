from character import Character

class Warrior(Character):
    #attributes
    __maxStamina = None
    __currentStamina = None
    __staminaRegeneration = None
    __strength = None
    __defensiveStance = None

    __attacks = None
    #end attributes

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

    # accessors
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

    # mutators
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

    # behaviours
    def chooseAttack(self, target):
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
                attackMethod(target)
            else:
                print(f"{self.getName()} got ready for a move, but was collapsed from exhaustion instead.")
        else:
            print("Invalid attack.")

    def lunge(self, target):
        output = []

        damage = self.getStrength() * 1.8 * target.getDefenseMultiplier()
        output.append(f"{self.getName()} lunges at {target.getName()} for {damage} damage!")
        target.takeDamage(damage)

        output.append(f"{self.getName()}'s lunge has left him exposed.")
        self.setExposedStatus(True)

        return output

    def slash(self, target):

        damage = self.__strength * target.getDefenseMultiplier()  # defense multiplier calculations were put in the skills damage calculations to more easily allow for defense shred
        print(f"{self.getName()} slashes at {target.getName()} for {damage} damage!")
        target.takeDamage(damage)

    def cleave(self, target):

        totalDamage = 0
        #for target in targets:
        damage = self.__strength + 10 * target.getDefenseMultiplier()
        totalDamage += damage
            #print(f"{self.name} cleaves {target} for {damage} damage!")
            #target.takeDamage(damage)
        print(f"{self.getName()} dealt a total of {totalDamage} damage with cleave!")
        target.takeDamage(totalDamage)

    def shieldBash(self, target):
        if self.getDefensiveStance() == True:
            print(f"{self.getName()}'s defensive stance enabled a more forceful shield bash!")
            damage = (self.getStrength() + 100 - 100*self.getDefenseMultiplier()) * target.getDefenseMultiplier()
        else:
            damage = self.getStrength() * target.getDefenseMultiplier()
        print(f"{self.getName()} shield bashes {target.getName()} for {damage} damage!")
        target.takeDamage(damage)

    def defensiveStance(self, target):
        self.setDefensiveStance(True)
        print(f"{self.getName()} takes a defensive stance, reducing incoming phyiscal damage.")
        damage = target.getDefenseMultiplier() * 5
        print(f"{target.getName()} is intimidated and takes {damage} damage!")
        target.takeDamage(damage)


    #turn based combat related behaviours
    def takeDamage(self, amount):
        if self.getDefensiveStance():
            amount = max(amount - (100 - 100 * self.getDefenseMultiplier()), 0)
            print(f"{self.getName()}'s defensive stance further reduced incoming damage to a total of {amount}!")

        if self.getExposedStatus():
            print(f"{self.getName()}'s exposed state rendered all armour inneffective.")
            amount = amount/self.getDefenseMultiplier() #gets the true damage value to deal true damage

        self.setCurrentHP(self.getCurrentHP() - amount)
        print(f"{self.getName()} has {self.getCurrentHP()} HP remaining")

    def upkeepPhase(self):
        self.setCurrentStamina(min(self.__maxStamina, self.__currentStamina + self.__staminaRegeneration))
        self.setExposedStatus(False) #stops being exposed upon next turn

        if self.getCursedStatus()["status"]:
            self.setCursedTimer(self.getCursedTimer() +1)
            if self.getCursedTimer() >= self.getCursedStatus()["delay"]:
                damage = self.getCursedStatus()["damage"]
                
                self.setCurrentHP(self.getCurrentHP() - damage)

                print(f"The curse has taken hold. {self.getName()} has suffered {damage} damage!")
                self.setCursedTimer(0)
                self.setCursedStatus(False, None, None)

                print(f"{self.getName()} has {self.getCurrentHP()} HP remaining")

            else:
                turnsLeft = self.getCursedStatus()["delay"] - self.getCursedTimer()
                print(f"\nThe curse manifests in {turnsLeft} more turn(s)...\n")

