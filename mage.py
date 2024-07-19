from character import Character
from textWriter import TextRenderer

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
        self.__attacks = { 
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
    def listAttacks(self, window, attackMenuArea, fontSize):
        attack_writer = TextRenderer(window, attackMenuArea, fontSize) 

        attack_list = ["Attack List:"]
        
        attackList = list(self.__attacks.items())
        for i, (attack, info) in enumerate(attackList): # Displays all attack info within the space outlined in the parameters
            attack_list.append(f"{i + 1}. {attack} (Mana cost: {info['manaCost']})")
        
        attack_writer.display_output(attack_list)

    def attack(self, target, chosen_attack):
        output = []
        
        attackList = list(self.__attacks.items())
        if 1 <= chosen_attack <= len(attackList):
            attack, attackInfo = attackList[chosen_attack - 1]
            if attack == 'Really Big Beam':
                self.reallyBigBeam(target)
            elif self.getCurrentMana() >= attackInfo["manaCost"]:
                remainingMana = self.getCurrentMana() - attackInfo["manaCost"]
                self.setCurrentMana(remainingMana)
                attackMethod = attackInfo["method"]
                attackOutput = attackMethod(target)
                output.extend(attackOutput)
            else:
                output.append(f"A lack of necessary mana for this attack resulted in {self.getName()} collapsing from spell backlash instead.")
        else:
            output.append("Invalid attack.")

        return output

    # attack functions
    def fireball(self, target):
        output = []

        # mana calcs
        attackInfo = self.__attacks["Fireball"]
        self.setCurrentMana(self.getCurrentMana() - attackInfo["manaCost"])

        # damage calcs
        damage = self.__magicPower * target.getMagicResistanceMultiplier()
        output.append(f"{self.getName()} shoots a fireball at {target.getName()} for {damage} damage!")
        damage_output = target.takeDamage(damage)
        output.extend(damage_output)

        return output

    def reallyBigBeam(self, target):
        output = []

        # mana calcs
        spentMana = int(input("How much mana do you channel into the beam? "))
        currentMana = self.getCurrentMana()
        while currentMana < spentMana:
            print("You don't have that much mana!")
            spentMana = int(input("Channel a different amount of mana into the beam or face spell backlash: "))

        output.append(f"{spentMana} mana was spent on this attack.")
        self.setCurrentMana(currentMana - spentMana)

        # damage calcs
        damage = self.__magicPower * spentMana * target.getMagicResistanceMultiplier()
        output.append(f"{self.getName()} unleashes a really big beam at {target.getName()} for {damage} damage!")
        damage_output = target.takeDamage(damage)
        output.extend(damage_output)

        return output

    def explosion(self, target):
        output = []

        # mana calcs
        attackInfo = self.__attacks["EXPLOSION!!!"] 
        spentMana = attackInfo["manaCost"] # track spent mana to scale damage off as there will be things that increase mana cost of this spell
        self.setCurrentMana(self.getCurrentMana() - spentMana)
        self.setManaStability(0)

        # damage calcs
        totalDamage = 0
        damage = self.getMagicPower() * spentMana * self.getMaxMana() * target.getMagicResistanceMultiplier() / target.getCurrentHP()
        totalDamage += damage

        output.append(f"{self.getName()}'s MASSIVE EXPLOSION dealt {totalDamage} total damage!")
        damage_output = target.takeDamage(totalDamage)
        output.extend(damage_output)

        return output

    def manaField(self, target):
        output = []

        # mana calcs
        attackInfo = self.__attacks["Mana Field"]
        manaCost = attackInfo["manaCost"]
        self.setCurrentMana(self.getCurrentMana() - manaCost)

        # sets MR to 15% and armour to 70%
        self.setMagicResistance(15/100)
        self.setDefenseMultiplier(70/100)
        output.append(f"{self.getName()} sets up a magic barrier. {self.getName()} now blocks 85% of incoming magic damage and 30% of incoming physical damage.")

        return output

    def magicGlock(self, target):
        output = []

        # mana calcs
        attackInfo = self.__attacks['"Magic" Glock']
        self.setCurrentMana(self.getCurrentMana() - attackInfo["manaCost"])

        # damage calcs
        damage = (self.getMagicPower() + 20) * target.getDefenseMultiplier()
        output.append(f"{self.getName()} pulls out a glock and taps the {target.getName()} with a quick flick to its head, pulverising its brains with {damage} damage!")
        damage_output = target.takeDamage(damage)
        output.extend(damage_output)

        return output

    # turn based combat features
    def takeDamage(self, amount):
        output = []
        self.setCurrentHP(self.getCurrentHP() - amount)
        output.append(f"{self.getName()} takes {amount} damage.")
        output.append(f"{self.getName()} has {self.getCurrentHP()} HP remaining")
        return output

    def upkeepPhase(self):
        self.setCurrentMana(min(self.__maxMana, self.__currentMana + self.__manaRegen))

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
