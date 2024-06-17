from character import Character

class Mage(Character):

    # attributes
    __maxMana = None
    __currentMana = None
    __magicPower = None
    __manaRegen = None
    __maxHP = None
    __currentHP = None
    __manaStability = None
    __attacks = None
    # end attributes

    # constructors
    def __init__(self, name, armour, magicResistance, magicPower):
        super().__init__(name, "Mage", armour, magicResistance)
        self.__maxMana = 100
        self.__magicPower = magicPower
        self.__currentMana = self.__maxMana
        self.__manaRegen = 10
        self.__maxHP = 100
        self.__currentHP = self.__maxHP
        self.__manaStability = 100  # should be percentage
        self.__attacks = {
            "Fireball": {"method": self.fireball, "manaCost": 15, "spellStability": 100},
            "Really Big Beam": {"method": self.reallyBigBeam, "manaCost": 'Variable', "spellStability": 'Variable'},
            "EXPLOSION!!!": {"method": self.explosion, "manaCost": 100, "spellStability": 0},
            "Mana Field": {"method": self.manaField, "manaCost": 30},  # defensive against magic attacks
            "Restore Magic Flux": {"method": self.restoreMagicFlux, "manaCost": 5, "spellStability": 100},
            '"Magic" Glock': {"method": self.magicGlock, "manaCost": 0, "spellStability": 100},
        }

    # accessors
    def getMagicPower(self):
        return self.__magicPower

    def getMaxMana(self):
        return self.__maxMana

    def getCurrentMana(self):
        return self.__currentMana

    def getManaRegen(self):
        return self.__manaRegen

    def getMaxHP(self):
        return self.__maxHP

    def getCurrentHP(self):
        return self.__currentHP

    def getManaStability(self):
        return self.__manaStability

    # mutators
    def setMagicPower(self, newMagicPower):
        self.__magicPower = newMagicPower

    def setMaxMana(self, newMaxMana):
        self.__maxMana = newMaxMana

    def setCurrentMana(self, newCurrentMana):
        self.__currentMana = newCurrentMana

    def setManaRegen(self, newManaRegen):
        self.__manaRegen = newManaRegen

    def setMaxHP(self, newMaxHP):
        self.__maxHP = newMaxHP

    def setCurrentHP(self, newCurrentHP):
        self.__currentHP = newCurrentHP

    def setManaStability(self, newManaStability):
        self.__manaStability = newManaStability

    # behaviours
    def chooseAttack(self, target):
        print(f"Choose an attack (Current mana: {self.__currentMana}):")
        attackList = list(self.__attacks.items())
        for i, (attack, info) in enumerate(attackList):
            print(f"{i + 1}. {attack} (Mana cost: {info['manaCost']})")
        chosenAttack = int(input("Enter the number of the attack: "))  # change this to a key press later
        if 1 <= chosenAttack <= len(attackList):
            attack, attackInfo = attackList[chosenAttack - 1]
            if self.__currentMana >= attackInfo["manaCost"]:
                attackMethod = attackInfo["method"]
                attackMethod(target)
            else:
                print("Not enough mana for this attack.")
        else:
            print("Invalid attack.")

    def regenerateMana(self):
        self.setCurrentMana(min(self.__maxMana, self.__currentMana + self.__manaRegen))

    # attack functions
    def fireball(self, target):
        # mana calcs
        attackInfo = self.__attacks["Fireball"]
        self.__currentMana -= attackInfo["manaCost"]
        self.__manaStability -= int(abs(attackInfo["spellStability"] - 100) / self.__currentMana)

        # damage calcs
        damage = self.__magicPower * target.defenseMultiplier
        print(f"{self.name} shoots a fireball at {target} for {damage} damage!")
        target.takeDamage(damage)

    def reallyBigBeam(self, target):
        # mana calcs
        spentMana = self.__currentMana  # find a way to make this variable later
        self.setCurrentMana(0)  # if mana value isn't a number such as 'x', all current mana will be consumed
        self.setManaStability(min(100, self.__manaStability - spentMana / self.__maxMana * 100))  # decreases mana stability by a ratio of how much mana you spent from your max
        print(f"{spentMana} was spent on this attack.")

        # damage calcs
        damage = self.__magicPower * spentMana - 100
        print(f"{self.name} unleashes a really big beam at {target} for {damage} damage!")
        target.takeDamage(damage)

    def explosion(self, targets):
        # mana calcs
        attackInfo = self.__attacks["EXPLOSION!!!"]
        spentMana = attackInfo["manaCost"]
        self.setCurrentMana(max(0, self.__currentMana - spentMana))  # bottom out
        self.setManaStability(0)
        print(f"{spentMana} was spent on this attack.")

        # damage calcs
        totalDamage = 0
        for target in targets:
            damage = self.__magicPower * target.magicResistanceMultiplier * target.currentHP  # Example: Cleave attack deals double the warrior's strength to each target
            totalDamage += damage
            print(f"{self.name} blows up {target} for {damage} damage!")
            target.takeDamage(damage)
        print(f"{self.name}'s MASSIVE EXPLOSION dealt {totalDamage} total damage!")

    def manaField(self):
        #mana calcs
        attackInfo = self.__attacks["Mana Field"]
        manaCost = attackInfo["manaCost"]
        self.setCurrentMana(self.getCurrentMana() - manaCost)
        self.setManaStability((100-attackInfo["spellStability"])/self.getCurrentMana)

        #sets MR to 15% and armour to 70%
        self.setMagicResistance(15/100)
        self.setArmor(70/100)

    def restoreMagicFlux(self):
        self.setManaStability(min(100, self.__manaStability + 50))  # mana stability should be a % so shouldn't exceed 100
        print(f"{self.name} discharges the surrounding flow of magic with a simple spell.")

    def magicGlock(self, target):
        # mana calcs
        attackInfo = self.__attacks['"Magic" Glock']
        self.__currentMana -= attackInfo["manaCost"]
        self.__manaStability -= int(abs(attackInfo["spellStability"] - 100) / self.__currentMana)

        # damage calcs
        damage = self.__magicPower * target.defenseMultiplier
        print(f"{self.name} shoots a fireball at {target} for {damage} damage!")
        target.takeDamage(damage)