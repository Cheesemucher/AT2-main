from character import Character

class Warrior(Character):
    __maxStamina = 100
    __currentStamina = None
    __staminaRegeneration = 10
    __strength = 15
    __maxHP = None
    __currentHP = None
    __attacks = None

    def __init__(self, name, maxHP):
        super().__init__(name, "Warrior", armor=10)
        self.__currentStamina = self.__maxStamina
        self.__maxHP = maxHP
        self.__currentHP = maxHP
        self.__attacks = {
            "Basic Attack": {"method": self.basicAttack, "staminaCost": 10},
            "Charge": {"method": self.charge, "staminaCost": 20},
            "Cleave Attack": {"method": self.cleaveAttack, "staminaCost": 30},
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

    def getMaxHP(self):
        return self.__maxHP

    def getCurrentHP(self):
        return self.__currentHP

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

    def setMaxHP(self, maxHP):
        self.__maxHP = maxHP

    def setCurrentHP(self, currentHP):
        self.__currentHP = currentHP

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
            if self.__currentStamina >= attackInfo["staminaCost"]:
                self.__currentStamina -= attackInfo["staminaCost"]
                attackMethod = attackInfo["method"]
                attackMethod(target)
            else:
                print("Not enough stamina for this attack.")
        else:
            print("Invalid attack.")

    def regenerateStamina(self):
        self.setCurrentStamina(min(self.__maxStamina, self.__currentStamina + self.__staminaRegeneration))

    def attack(self, target):
        # Calculate damage based on warrior's level, strength, and any weapon modifiers
        # For simplicity, let's assume the warrior's damage is directly proportional to their level
        damage = self.__strength * self.level
        target.takeDamage(damage)  # Apply damage to the target
        return damage  # Return the amount of damage dealt

    def charge(self, target):
        print(f"{self.name} charges towards {target.name}!")
        target.takeDamage(self.__strength)  # Example: Charge deals damage equal to the warrior's strength

    def basicAttack(self, target):
        damage = self.__strength * target.defenseMultiplier  # defense multiplier calculations were put in the skills damage calculations to more easily allow for defense shred
        print(f"{self.name} performs a basic attack on {target} for {damage} damage!")
        target.takeDamage(damage)

    def cleaveAttack(self, targets):
        totalDamage = 0
        for target in targets:
            damage = self.__strength * 2  # Example: Cleave attack deals double the warrior's strength to each target
            totalDamage += damage
            print(f"{self.name} cleaves {target} for {damage} damage!")
            target.takeDamage(damage)
        print(f"{self.name} dealt a total of {totalDamage} damage with cleave!")

    def shieldBash(self, target):
        damage = self.__strength + 5  # Example: Shield bash deals warrior's strength plus 5 additional damage
        print(f"{self.name} performs a shield bash on {target} for {damage} damage!")
        target.takeDamage(damage)

    def defensiveStance(self):
        self.armorClass += 5  # Example: Defensive stance increases armor class by 5
        print(f"{self.name} enters a defensive stance, increasing armor class!")
