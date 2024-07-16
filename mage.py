from character import Character

class Mage(Character):

    # attributes
    __maxMana = None
    __currentMana = None
    __magicPower = None
    __manaRegen = None
    #__manaStability = None
    __attacks = None
    # end attributes

    # constructors
    def __init__(self, name):
        super().__init__(name, "Mage", 90, 80)
        self.__maxMana = 100
        self.__magicPower = 50
        self.__currentMana = self.__maxMana
        self.__manaRegen = 10
        self.__manaStability = 100  # should be percentage
        self.__attacks = { #decomissioned:            "Restore Magic Flux": {"method": self.restoreMagicFlux, "manaCost": 5, "spellStability": 100},
            "Fireball": {"method": self.fireball, "manaCost": 15, "spellStability": 100},
            "Really Big Beam": {"method": self.reallyBigBeam, "manaCost": 'Variable', "spellStability": 'Variable'},
            "EXPLOSION!!!": {"method": self.explosion, "manaCost": 100, "spellStability": 0},
            "Mana Field": {"method": self.manaField, "manaCost": 30},  # defensive against magic attacks
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

    def setManaStability(self, newManaStability):
        self.__manaStability = newManaStability

    # behaviours
    def chooseAttack(self, target):
        self.setExposedStatus(False)
        
        attackSelected = False
        while attackSelected == False:
            print(f"Choose an attack (Current mana: {self.__currentMana}):")
            attackList = list(self.__attacks.items())
            for i, (attack, info) in enumerate(attackList):
                print(f"{i + 1}. {attack} (Mana cost: {info['manaCost']})")
            chosenAttack = int(input("Enter the number of the attack: "))  # change this to a key press later
            if 1 <= chosenAttack <= len(attackList):
                attack, attackInfo = attackList[chosenAttack - 1]
                if attack == 'Really Big Beam' or self.__currentMana >= attackInfo["manaCost"]:
                    print()
                    attackMethod = attackInfo["method"]
                    attackMethod(target)
                    attackSelected = True
                else:
                    print(f"A lack of necessary mana for this attack resulted in {self.getName()} to collapse from spell backlash instead.")
            else:
                print("\nInvalid attack.\n")

    # attack functions
    def fireball(self, target):
        # mana calcs
        attackInfo = self.__attacks["Fireball"]
        self.setCurrentMana(self.getCurrentMana() - attackInfo["manaCost"])
        #self.__manaStability -= int(abs(attackInfo["spellStability"] - 100) / self.__currentMana)

        # damage calcs
        damage = self.__magicPower * target.getMagicResistanceMultiplier()
        print(f"{self.getName()} shoots a fireball at {target.getName()} for {damage} damage!")
        target.takeDamage(damage)

    def reallyBigBeam(self, target):
        # mana calcs
        #spentMana = self.__currentMana  # find a way to make this variable later
        spentMana = int(input("How much mana do you channel into the beam? "))
        currentMana = self.getCurrentMana()
        while currentMana < spentMana:
            print("You don't have that much mana!")
            spentMana = int(input("Channel a different amount of mana into the beam or face spell backlash: "))

        #self.setManaStability(min(100, self.__manaStability - spentMana / self.__maxMana * 100))  # decreases mana stability by a ratio of how much mana you spent from your max
        print(f"{spentMana} mana was spent on this attack.")
        self.setCurrentMana(currentMana - spentMana)

        # damage calcs
        damage = self.__magicPower * spentMana * target.getMagicResistanceMultiplier()
        print(f"{self.getName()} unleashes a really big beam at {target.getName()} for {damage} damage!")
        target.takeDamage(damage)

    def explosion(self, target):
        # mana calcs
        attackInfo = self.__attacks["EXPLOSION!!!"] 
        spentMana = attackInfo["manaCost"] #track spent mana to scale damage off as there will be things that increase mana cost of this spell
        self.setCurrentMana(self.getCurrentMana() - spentMana)
        self.setManaStability(0)

        # damage calcs
        totalDamage = 0
        #for target in targets:
        damage = self.getMagicPower() * spentMana * self.getMaxMana() * target.getMagicResistanceMultiplier() / target.getCurrentHP()
        totalDamage += damage
        #print(f"{self.getName()} blows up {target.getName()} for {damage} damage!")
        #target.takeDamage(damage)

        print()
        print(f"{self.getName()}'s MASSIVE EXPLOSION dealt {totalDamage} total damage!")
        target.takeDamage(totalDamage)

    def manaField(self, target):
        #mana calcs
        attackInfo = self.__attacks["Mana Field"]
        manaCost = attackInfo["manaCost"]
        self.setCurrentMana(self.getCurrentMana() - manaCost)
        #self.setManaStability((100-attackInfo["spellStability"])/self.getCurrentMana)

        #sets MR to 15% and armour to 70%
        self.setMagicResistance(15/100)
        self.setDefenseMultiplier(70/100)
        print(f"\n{self.getName()} sets up a magic barrier. {self.getName()} now blocks 85% of incoming magic damage and 30% of incoming physical damage.")

    def restoreMagicFlux(self, target): #decomissioned
        self.setManaStability(min(100, self.__manaStability + 50))  # mana stability should be a % so shouldn't exceed 100
        print(f"{self.getName()} discharges the surrounding flow of magic with a simple spell.")

    def magicGlock(self, target):
        # mana calcs
        attackInfo = self.__attacks['"Magic" Glock']
        self.setCurrentMana(self.getCurrentMana() - attackInfo["manaCost"])
        self.__manaStability -= int(abs(attackInfo["spellStability"] - 100) / self.__currentMana)

        # damage calcs
        damage = (self.getMagicPower() + 20) * target.getDefenseMultiplier()
        print(f"\n{self.getName()} pulls out a glock and taps the {target.getName()} with a quick flick to its head, pulverising it's brains with {damage} damage!")
        target.takeDamage(damage)


    #turn based combat features
    def takeDamage(self, amount):
        self.setCurrentHP(self.getCurrentHP() - amount)
        print(f"{self.getName()} has {self.getCurrentHP()} HP remaining")

    def upkeepPhase(self):
        self.setCurrentMana(min(self.__maxMana, self.__currentMana + self.__manaRegen))