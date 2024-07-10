from mage import Mage
from warrior import Warrior
from ninja import Ninja
from goblin import Goblin
from skeleton import Skeleton
import time

# simulated combat between a character and an enemy

print("choices are: Warrior, Mage, Ninja")
playerChoice = input("What class do you choose? ")
name = input("What are you called? ")

if playerChoice == "Mage":
    player = Mage(name, 90, 80, 50) #name, armour multiplier, MR multiplier, Magic Power
elif playerChoice == "Warrior":
    player = Warrior(name, 60, 80, 50)
elif playerChoice == "Ninja":
    player = Ninja(name, 90, 100, 45) #name, armour multiplier,  MR, strength

goblin = Goblin(80, 95, 60, None) #armour, MR, strength, magic power
skeleton = Skeleton(80, 90, 50, 50)
#image to load:
#'pygame.image.load("assets/goblin.png").convert_alpha()'


while player.isAlive() and skeleton.isAlive():
    print()
    if player.isAlive():
        player.chooseAttack(skeleton)
        print()

    player.upkeepPhase()
    time.sleep(1)

    if skeleton.isAlive():
        print()
        skeleton.attack(player)

    

if player.isAlive() == False:
    print(f"{player.getName()} has died")

elif skeleton.isAlive() == False:
    print(f"{skeleton.getName()} has been killed.")