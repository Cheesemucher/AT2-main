from game import Game
from mage import Mage
from warrior import Warrior
from ninja import Ninja
from goblin import Goblin
from skeleton import Skeleton
import time

class Combat():
    #attributes
    __enemy = None
    __player_class = None
    __player = None

    def __init__(self, player_class, enemy):
        self.__player_class = player_class
        self.__enemy = enemy
        self.__player = self.__player_class()

    #accessors
    def getEnemy(self):
        return self.__enemy

    def getPlayerclass(self):
        return self.__player_class

    def getPlayer(self):
        return self.__player


    #mutators
    def setEnemy(self, newEnemy):
        self.__enemy = newEnemy

    def setPlayerclass(self, newPlayerclass):
        self.__player_class = newPlayerclass

    def setPlayer(self, newPlayer):
        self.__player = newPlayer


    
    #throws user into a loop of turn based battle to the death
    def enter_battle(self):
        player = self.getPlayer()
        enemy = self.getEnemy()

        while player.isAlive() and enemy.isAlive(): #repeats until either party dies
            print()
            if player.isAlive():
                player.chooseAttack(enemy)
                print()

            player.upkeepPhase() # counts a turn to have passed, triggering all regeneration and ticking up all status effect timers
            time.sleep(1)

            if enemy.isAlive(): #identical turn but for the enemy but without an upkeep step as the enemy does not get to regenerate
                print()
                enemy.attack(player)

        # check who died for the while loop to break
        if player.isAlive() == False:
            print(f"{player.getName()} has died")

        elif enemy.isAlive() == False:
            print(f"{enemy.getName()} has been killed.")