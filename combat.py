import pygame
from assets import GAME_ASSETS
import time
from textWriter import TextRenderer

class Combat:
    # Attributes
    __enemy = None
    __player = None
    __map_image = None
    __window = None
    __player_image = None
    __enemy_image = None
    __text_renderer = None

    def __init__(self, player, enemy, window, player_image):
        self.__enemy = enemy
        self.__player = player
        self.__window = window
        self.__map_image = pygame.image.load(GAME_ASSETS["arena"]).convert_alpha()
        self.__map_image = pygame.transform.scale(self.__map_image, (800, 600))
        self.__player_image = pygame.transform.scale(player_image, (100, 150))
        self.__enemy_image = pygame.transform.scale(self.__enemy.getImage(), (100, 150))
        self.__text_renderer = TextRenderer(window, pygame.Rect(310, 70, 210, 500)) # make a TextRenderer object for writing in the background place

    # Accessors
    def getEnemy(self):
        return self.__enemy

    def getMapImage(self):
        return self.__map_image

    def getPlayer(self):
        return self.__player

    def getWindow(self):
        return self.__window

    def getPlayerImage(self):
        return self.__player_image

    def getEnemyImage(self):
        return self.__enemy_image

    def getTextRenderer(self):
        return self.__text_renderer

    # Mutators
    def setEnemy(self, newEnemy):
        self.__enemy = newEnemy
        self.__enemy_image = pygame.transform.scale(self.__enemy.getImage(), (100, 150))

    def setMapImage(self, newMapImage):
        self.__map_image = newMapImage

    def setPlayer(self, newPlayer):
        self.__player = newPlayer
        self.__player_image = pygame.transform.scale(self.__player.getImage(), (100, 150))

    def setWindow(self, newWindow):
        self.__window = newWindow

    def setPlayerImage(self, newPlayerImage):
        self.__player_image = newPlayerImage

    def setEnemyImage(self, newEnemyImage):
        self.__enemy_image = newEnemyImage

    def setTextRenderer(self, newTextRenderer):
        self.__text_renderer = newTextRenderer

    # Throws user into a loop of turn-based battle to the death
    def enter_battle(self):
        player = self.getPlayer()
        enemy = self.getEnemy()

        if player is None or enemy is None:
            print(f"Error: player or enemy is None. player: {player}, enemy: {enemy}")
            return

        while player.isAlive() and enemy.isAlive():  # Repeats combat loop until either party dies

            output = player.chooseAttack(enemy)  # Player takes action
            self.__text_renderer.display_output(output) # Writes every item stored in output onto the screen

            pygame.display.flip()
            time.sleep(2)

            self.__window.fill((0, 0, 0))  # Clear the console for the enemy's turn
            self.draw_arena()  # Draw the arena

            if not enemy.isAlive():  # Checks whether the enemy has died
                self.__text_renderer.write_text(f"{enemy.getName()} has been killed.")
                pygame.display.flip()
                time.sleep(2)
                return player  # Return the updated player information to wherever 'combat' was called

            output = player.upkeepPhase()  # Counts a turn to have passed, triggering all regeneration and ticking up all status effect timers
            self.__text_renderer.display_output(output)

            time.sleep(1)

            output = enemy.attack(player)  # Enemy takes action
            self.__text_renderer.display_output(output) # Enemy action's outputs are displayed

            pygame.display.flip()
            time.sleep(2)

            self.__window.fill((0, 0, 0))  # Clear the console again for player's turn
            self.draw_arena()  # Draw the arena again

            if not player.isAlive():
                self.__text_renderer.write_text(f"{player.getName()} has died")
                time.sleep(1)
                self.__window.blit(pygame.image.load(GAME_ASSETS["lose_screen"]).convert_alpha(), (0, 0))
                pygame.display.flip()


    def draw_arena(self):
        window = self.getWindow()

        window.blit(self.__map_image, (0, 0))
        window.blit(self.__player_image, (150, (window.get_height() - self.__player_image.get_height()) / 2))
        window.blit(self.__enemy_image, (650, (window.get_height() - self.__enemy_image.get_height()) / 2))
        pygame.display.flip()
