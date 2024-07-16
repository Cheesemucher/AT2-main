import pygame
from assets import GAME_ASSETS
from mage import Mage
from warrior import Warrior
from ninja import Ninja
from goblin import Goblin
from skeleton import Skeleton
import time

class Combat:
    # Attributes
    __enemy = None
    __player = None
    __map_image = None
    __window = None

    def __init__(self, player, enemy, window):
        self.__enemy = enemy
        self.__player = player
        self.__window = window
        self.__map_image = pygame.image.load(GAME_ASSETS["arena"]).convert_alpha()
        self.__map_image = pygame.transform.scale(self.__map_image, (800, 600)) # rescale the image to fit the 800x600 window.

    # Accessors
    def getEnemy(self):
        return self.__enemy

    def getMapImage(self):
        return self.__map_image

    def getPlayer(self):
        return self.__player

    def getWindow(self):
        return self.__window

    # Mutators
    def setEnemy(self, newEnemy):
        self.__enemy = newEnemy

    def setMapImage(self, newMapImage):
        self.__map_image = newMapImage

    def setPlayer(self, newPlayer):
        self.__player = newPlayer

    def setWindow(self, newWindow):
        self.__window = newWindow


    #behaviours

    # Function to replace print() that displays combat text on the visual terminal paper
    def display_text(self, text):
            text_surface = self.__font.render(text, True, (255, 255, 255))  # Render the text
            self.__window.blit(text_surface, (400,100))  # Draw the text on the window where the blank paper area at the bottom of the screen is.

    # Throws user into a loop of turn-based battle to the death
    def enter_battle(self):
        player = self.getPlayer()
        enemy = self.getEnemy()

        while player.isAlive() and enemy.isAlive():  # Repeats until either party dies
            print()

            output = player.chooseAttack(enemy)  # Player takes action
            for event in output:
                self.display_text(event)

            print()
            if not enemy.isAlive():  # Checks whether the enemy has died
                print(f"{enemy.getName()} has been killed.")
                return player  # Return the updated player information to wherever 'combat' was called

            player.upkeepPhase()  # Counts a turn to have passed, triggering all regeneration and ticking up all status effect timers
            time.sleep(1)

            print()
            enemy.attack(player)  # Enemy takes action

            if not player.isAlive():
                print(f"{player.getName()} has died")
                self.getWindow().blit(pygame.image.load(GAME_ASSETS["lose_screen"]).convert_alpha())


    def draw_arena(self, player_image):
        """
        Draws a separate map for the enemy and player to fight on
        """

        player_image = pygame.transform.scale(player_image, (player_image.get_width() * 3, player_image.get_height() * 3)) # Scale the character image to required dimensions

        window = self.getWindow()

        window.blit(self.__map_image, (0, 0))
        window.blit(player_image, (150, window.get_height() / 2))
        self.getEnemy().draw([550 - self.getEnemy().getImage().get_width(), window.get_height() / 2], 3)
        pygame.display.flip()
