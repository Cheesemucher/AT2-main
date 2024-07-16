import random
import pygame
from assets import GAME_ASSETS
from combat import Combat
from goblin import Goblin
from skeleton import Skeleton
from warrior import Warrior
from mage import Mage
from ninja import Ninja

class Map:
    __player = None
    __window = None
    __map_image = None
    __player_images = None
    __player_type = None
    __player_position = None
    __enemies = None
    __in_combat = False
    __current_enemy = None
    __blue_orb = None
    __game_over = False
    __orb_position = None
    __entity_proportions = (40, 30)  # Desired width and height for character images

    def __init__(self, window):
        """
        Initialize the Map class.

        Args:
            window (pygame.Surface): The game window surface.
        """
        self.__window = window
        self.__map_image = pygame.image.load(GAME_ASSETS["dungeon_map"]).convert_alpha()
        self.__map_image = pygame.transform.scale(self.__map_image, (self.__window.get_width(), self.__window.get_height()))
        self.__player_images = {
            'Warrior': pygame.image.load(GAME_ASSETS['warrior']).convert_alpha(),
            'Mage': pygame.image.load(GAME_ASSETS['mage']).convert_alpha(),
            'Ninja': pygame.image.load(GAME_ASSETS["ninja"]).convert_alpha()
        }
        self.__player_position = [self.__window.get_width() / 2, self.__window.get_height() / 2]
        self.__enemies = [
            Goblin([50, 50], self.__window),
            Skeleton([self.__window.get_width() - 120, 50], self.__window)
        ]

    # Accessors
    def get_player(self):
        return self.__player

    def get_window(self):
        return self.__window

    def get_map_image(self):
        return self.__map_image

    def get_player_images(self):
        return self.__player_images

    def get_player_type(self):
        return self.__player_type

    def get_player_position(self):
        return self.__player_position

    def get_enemies(self):
        return self.__enemies

    def get_in_combat(self):
        return self.__in_combat

    def get_current_enemy(self):
        return self.__current_enemy

    def get_blue_orb(self):
        return self.__blue_orb

    def get_game_over(self):
        return self.__game_over

    def get_orb_position(self):
        return self.__orb_position

    def get_entity_proportions(self):
        return self.__entity_proportions

    # Mutators
    def set_player(self, new_player):
        self.__player = new_player

    def set_window(self, new_window):
        self.__window = new_window

    def set_map_image(self, new_map_image):
        self.__map_image = new_map_image

    def set_player_images(self, new_player_images):
        self.__player_images = new_player_images

    def set_player_type(self, new_player_type):
        self.__player_type = new_player_type

    def set_player_position(self, new_player_position):
        self.__player_position = new_player_position

    def set_enemies(self, new_enemies):
        self.__enemies = new_enemies

    def set_in_combat(self, new_in_combat):
        self.__in_combat = new_in_combat

    def set_current_enemy(self, new_current_enemy):
        self.__current_enemy = new_current_enemy

    def set_blue_orb(self, new_blue_orb):
        self.__blue_orb = new_blue_orb

    def set_game_over(self, new_game_over):
        self.__game_over = new_game_over

    def set_orb_position(self, new_orb_position):
        self.__orb_position = new_orb_position

    def set_entity_proportions(self, new_entity_proportions):
        self.__entity_proportions = new_entity_proportions

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
        self.__player = character_classes[character_type]("name")

    def check_for_combat(self):
        """
        Check if the player is in combat with any enemy.

        Returns:
            bool: True if the player is in combat, False otherwise.
        """
        for enemy in self.__enemies:
            if pygame.math.Vector2(enemy.getPosition()).distance_to(self.__player_position) < 50:
                self.__in_combat = True
                self.__current_enemy = enemy
                return True
        return False

    def handle_combat(self):
        """
        Trigger a battle and send the "current enemy" and "player" objects over to the combat class for the duration of the battle
        """
        if self.__in_combat and self.__current_enemy:
            battle = Combat(self.__player, self.__current_enemy, self.__window)
            battle.draw_arena(self.__player_image)
            self.__player = battle.enter_battle()  # Receive the updated player information after the battle

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
            self.__game_over = True
            print("YOU WIN")  # This can be modified to a more visual display if needed.
            return True
        return False

    def handle_events(self):
        """
        Handle user input events.
        
        Returns:
            str: 'quit' if the game is over and should be exited, None otherwise.
        """
        if self.__game_over:
            return 'quit'  # Stop processing events if game is over

        keys = pygame.key.get_pressed()
        move_speed = 2
        if keys[pygame.K_LEFT]:
            self.__player_position[0] -= move_speed
        if keys[pygame.K_RIGHT]:
            self.__player_position[0] += move_speed
        if keys[pygame.K_UP]:
            self.__player_position[1] -= move_speed
        if keys[pygame.K_DOWN]:
            self.__player_position[1] += move_speed

        if not self.__in_combat:
            if self.check_for_combat():
                return
        self.handle_combat()

        if self.__blue_orb and self.check_orb_collision():
            return 'quit'

    def draw(self):
        """
        Draw the game objects on the window.
        """
        self.__window.fill((0, 0, 0))
        self.__window.blit(self.__map_image, (0, 0))
        self.__window.blit(self.__player_image, (self.__player_position[0], self.__player_position[1]))
        for enemy in self.__enemies:
            enemy.draw(None, 1)
        if self.__blue_orb:
            self.__window.blit(self.__blue_orb, self.__orb_position)
        pygame.display.flip()
