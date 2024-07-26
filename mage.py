from character import Character
from textWriter import TextRenderer
from bar import Bar

class Mage(Character):

    # attributes
    __maxMana = None
    __currentMana = None
    __magicPower = None
    __manaRegen = None
    __attacks = None
    __stats = None
    # end attributes

    # constructors
    def __init__(self, name, window):
        super().__init__(name, "Mage", 90, 80, window)
        self.__maxMana = 100
        self.__magicPower = 60
        self.__currentMana = self.__maxMana
        self.__manaRegen = 50
        self.__player_health_bar = Bar(window, self, (10,10), "HP") # Make a bar object to track players health
        self.__player_resource_bar = Bar(window, self, (10,40), "Mana") # Make a bar object to track players stamina/mana
        self.__attacks = { 
            "Fireball": {"method": self.fireball, "manaCost": 15},
            #"Really Big Beam": {"method": self.reallyBigBeam, "manaCost": 'Variable'}, 
            "EXPLOSION!!!": {"method": self.explosion, "manaCost": 100},
            "Mana Field": {"method": self.manaField, "manaCost": 30},  # defensive against magic attacks
            '"Magic" Glock': {"method": self.magicGlock, "manaCost": 0},
        }
        self.__stats = {            
            "Mana Regen Rate":self.getManaRegen(),
            "Magic Power":self.getMagicPower(),
            "Max Mana":self.getMaxMana(),
            "Current Mana": self.getCurrentMana(),
            "Max HP":self.getMaxHP(),
            "Current HP": self.getCurrentHP(),
            "Defense Multiplier": self.getDefenseMultiplier(),
            "Magic Resistance Multiplier": self.getMagicResistance()
        }

    # accessors
    def getMagicPower(self):
        return self.__magicPower

    def getMaxMana(self):
        return self.__maxMana

    def getCurrentMana(self):
        return self.__currentMana

    def getManaRegen(self):
        return self.__manaRegen + (2 * self.getLevel())
    
    def getStats(self):
        self.__stats = { # update stat values
            "Mana Regen Rate":self.getManaRegen(),
            "Magic Power":self.getMagicPower(),
            "Max Mana":self.getMaxMana(),
            "Current Mana": self.getCurrentMana(),
            "Max HP":self.getMaxHP(),
            "Current HP": self.getCurrentHP(),
            "Defense Multiplier": self.getDefenseMultiplier(),
            "Magic Resistance Multiplier": self.getMagicResistance()
        }

        return self.__stats
    
    def getPlayerHealthBar(self):
        return self.__player_health_bar

    def getPlayerResourceBar(self):
        return self.__player_resource_bar

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
                attackMethod = attackInfo["method"]
                attackOutput = attackMethod(target)
                output.extend(attackOutput)
            else:
                output.append(f"A lack of necessary mana for this attack resulted in {self.getName()} collapsing from spell backlash instead.")
        else:
            output.append("Invalid attack.")

        self.getPlayerResourceBar().update_quantity() # Update the stamina/mana bar  

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

        if self.getExposedStatus()[0]: # Being in a defensive stance counters exposed status effects
            output.append(f"{self.getName()}'s exposed state rendered all armor ineffective.")
            amount = amount / self.getDefenseMultiplier()

        self.setCurrentHP(self.getCurrentHP() - amount)
        output.append(f"{self.getName()} takes {amount} damage.")
        output.append(f"{self.getName()} has {self.getCurrentHP()} HP remaining")

        self.getPlayerHealthBar().update_quantity() # Update the health bar to show new HP

        return output

    def upkeepPhase(self):
        output = ["End of turn: "]

        self.setCurrentMana(min(self.__maxMana, self.__currentMana + self.__manaRegen))
        output.append(f"{self.getName()} has regenerated {self.__manaRegen} mana.")
        self.__player_resource_bar.update_quantity()
        
        if self.getExposedStatus()[1] == 0:
            self.setExposedStatus(False, None)  # stops being exposed upon next turn
            output.append(f"{self.getName()} is no longer exposed!")
        elif self.getExposedStatus()[1]:
            self.setExposedStatus(True, self.getExposedStatus()[1] - 1)
            output.append(f"{self.getName()} remains exposed for another {self.getExposedStatus()[1]} turns.")

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
