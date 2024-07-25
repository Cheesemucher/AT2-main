import random
import pygame
from bar import Bar
from assets import GAME_ASSETS
from combat import Combat
from warrior import Warrior
from mage import Mage
from ninja import Ninja

class Map:
    __player = None
    __window = None
    __map_image = None
    __player_images = None
    __player_image = None
    __player_type = None
    __player_position = None
    __enemies = None
    __in_combat = False
    __current_enemy = None
    __blue_orb = None
    __game_over = False
    __orb_position = None
    __entity_proportions = None 

    def __init__(self, window, image, enemiesList):
        """
        Initialize the Map class.

        Args:
            window (pygame.Surface): The game window surface.
        """
        self.__window = window
        self.__map_image = pygame.transform.scale(image, (window.get_width(), window.get_height()))
        self.__player_images = {
            'Warrior': pygame.image.load(GAME_ASSETS['warrior']).convert_alpha(),
            'Mage': pygame.image.load(GAME_ASSETS['mage']).convert_alpha(),
            'Ninja': pygame.image.load(GAME_ASSETS["ninja"]).convert_alpha()
        }
        self.__entity_proportions = (60, 50)
        self.__player_position = [(self.__window.get_width() - self.__entity_proportions[0])/2, self.__window.get_height() / 2 + 200] # Gives the player an initial position in the bottom-middle area of the screen
        self.__enemies = enemiesList
        

    # Accessors
    def getPlayer(self):
        return self.__player

    def getWindow(self):
        return self.__window

    def getMapImage(self):
        return self.__map_image

    def getPlayerImages(self):
        return self.__player_images

    def getPlayerImage(self):
        return self.__player_image

    def getPlayerType(self):
        return self.__player_type

    def getPlayerPosition(self):
        return self.__player_position

    def getEnemies(self):
        return self.__enemies

    def getInCombat(self):
        return self.__in_combat

    def getCurrentEnemy(self):
        return self.__current_enemy

    def getBlueOrb(self):
        return self.__blue_orb

    def getGameOver(self):
        return self.__game_over

    def getOrbPosition(self):
        return self.__orb_position

    def getEntityProportions(self):
        return self.__entity_proportions

    # Mutators
    def setPlayer(self, new_player):
        self.__player = new_player

    def setWindow(self, new_window):
        self.__window = new_window

    def setMapImage(self, new_map_image):
        self.__map_image = new_map_image

    def setPlayerImages(self, new_player_images):
        self.__player_images = new_player_images

    def setPlayerImage(self, new_player_image):
        self.__player_image = new_player_image

    def setPlayerType(self, new_player_type):
        self.__player_type = new_player_type

    def setPlayerPosition(self, new_player_position):
        self.__player_position = new_player_position

    def setEnemies(self, new_enemies):
        self.__enemies = new_enemies

    def setInCombat(self, new_in_combat):
        self.__in_combat = new_in_combat

    def setCurrentEnemy(self, new_current_enemy):
        self.__current_enemy = new_current_enemy

    def setBlueOrb(self, new_blue_orb):
        self.__blue_orb = new_blue_orb

    def setGameOver(self, new_game_over):
        self.__game_over = new_game_over

    def setOrbPosition(self, new_orb_position):
        self.__orb_position = new_orb_position

    def setEntityProportions(self, new_entity_proportions):
        self.__entity_proportions = new_entity_proportions


    # Behaviors

    def load_player(self, character_type):
        """
        Load the player character.

        Args:
            character_type (str): The type of character to load.
        """
        character_classes = {
            'Warrior': Warrior,
            'Mage': Mage,
            'Ninja': Ninja
        }
        self.__player_type = character_type
        self.__player_image = self.__player_images[character_type]  # Assigns the player an image according to the selected class
        self.__player_image = pygame.transform.scale(self.__player_image, self.__entity_proportions) # Scale the character image to required dimensions
        
        # Instantiate the player object using the correct class
        self.__player = character_classes[character_type]("name", self.__window)

    def check_for_combat(self):
        """
        Check if the player is in combat with any enemy.

        Returns:
            bool: True if the player is in combat, False otherwise.
        """
        for enemy in self.__enemies:
            position = enemy.getPosition()
            if isinstance(position, (tuple, list)) and len(position) == 2: # To stop python from checking for the vectors to enemy positions
                if pygame.math.Vector2(position).distance_to(self.__player_position) < 50:
                    self.__in_combat = True
                    self.__current_enemy = enemy
                    return True

        return False

    def handle_combat(self):
        """
        Trigger a battle and send the "current enemy" and "player" objects over to the combat class for the duration of the battle
        """
        if self.__in_combat and self.__current_enemy:
            battle = Combat(self.__player, self.__current_enemy, self.__window, self.__player_image)
            battle.draw_arena()
            self.__player = battle.enter_battle()  # Receive the updated player information after the battle

            self.__enemies.remove(self.__current_enemy) # Take the dead enemy from the map's enemy list
            if not self.__enemies:
                self.spawn_blue_orb()

            # Reset combat state after combat ends
            self.__in_combat = False
            self.__current_enemy = None

            self.draw()

    def spawn_blue_orb(self):
        """
        Spawn the blue orb in the center of the map.
        """
        self.__blue_orb = pygame.image.load(GAME_ASSETS["blue_orb"]).convert_alpha()
        self.__blue_orb = pygame.transform.scale(self.__blue_orb, (50, 50))
        self.__orb_position = [self.__window.get_width() / 2 - 25, self.__window.get_height() / 2 - 25]

    def check_orb_collision(self):
        """
        Check if the player has collided with the blue orb.

        Returns:
            bool: True if the player has collided with the blue orb, False otherwise.
        """
        if self.__blue_orb and pygame.math.Vector2(self.__orb_position).distance_to(self.__player_position) < 25:
            print("Stage passed")  # This can be modified to a more visual display if needed.
            return True
        return False

    def handle_events(self):
        """
        Handle user input events.
        
        Returns:
            str: 'quit' if the game is over and should be exited, None otherwise.
        """

        keys = pygame.key.get_pressed()
        move_speed = 5

        if keys[pygame.K_LEFT]:
            self.__player_position[0] -= move_speed
            if self.__player_position[0] <= 0:  # Ensure you do not leave border
                self.__player_position[0] = 0  # Set position to the border if you do

        if keys[pygame.K_RIGHT]:
            self.__player_position[0] += move_speed
            if self.__player_position[0] + self.__entity_proportions[0] >= self.__window.get_width():  # Check against the right edge including player width
                self.__player_position[0] = self.__window.get_width() - self.__entity_proportions[0]

        if keys[pygame.K_UP]:
            self.__player_position[1] -= move_speed
            if self.__player_position[1] <= 0:
                self.__player_position[1] = 0
        if keys[pygame.K_DOWN]:
            self.__player_position[1] += move_speed
            if self.__player_position[1] + self.__entity_proportions[1] >= self.__window.get_height():
                self.__player_position[1] = self.__window.get_height() - self.__entity_proportions[1]
        
        if not self.__in_combat:
            if self.check_for_combat():
                return
        self.handle_combat()

        if self.__blue_orb and self.check_orb_collision():
            return 'next'

    def draw(self):
        """
        Draw the game objects on the window.
        """
        self.__window.fill((0, 0, 0))
        self.__window.blit(self.__map_image, (0, 0))
        self.__window.blit(self.__player_image, (self.__player_position[0], self.__player_position[1]))
        self.__player.getPlayerLevelBar().update_quantity()
        for enemy in self.__enemies:
            enemy.draw(None, self.__entity_proportions)
        if self.__blue_orb:
            self.__window.blit(self.__blue_orb, self.__orb_position)
        pygame.display.flip()
