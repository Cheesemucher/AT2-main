import pygame
from menu import MainMenu
from character_select import CharacterSelect
from map import Map
from goblin import Goblin
from skeleton import Skeleton
from wraith import Wraith
from evil_dark_sorc import EvilSorceror
from assets import load_assets, GAME_ASSETS

class Game:
    # Attributes
    __window = None  # the 'window' that the game will be displayed on
    __menu = None  # main menu
    __character_select = None  # character selection
    __game_maps = None  # actual map for the game
    __state = None  # which state the game is actually in (e.g., menu, character select, etc.)
    __current_character = None  # To store the chosen character
    __current_stage = None
    # End attributes

    def __init__(self):
        pygame.init()
        load_assets()  # load the game image assets
        self.__window = pygame.display.set_mode((800,600))
        self.__menu = MainMenu(self.__window)  # Create an instance of the MainMenu class
        self.__character_select = CharacterSelect(self.__window)  # Create an instance of the CharacterSelect class
        self.__state = 'menu'  # Set the initial state to 'menu'
        self.__current_stage = 0
        self.__game_maps = [ # Stores an instance of the Map class for each stage in the game
            Map(self.__window, pygame.image.load(GAME_ASSETS["dungeon_map"]).convert_alpha(), [Goblin([50, 50], self.__window, 2), Skeleton([self.__window.get_width() - 120, 50], self.__window, 3)]), 
            Map(self.__window, pygame.image.load(GAME_ASSETS["torture_map"]).convert_alpha(), [Wraith(None, self.__window, 3 + i) for i in range(3)]),
            Map(self.__window, pygame.image.load(GAME_ASSETS["graveyard_map"]).convert_alpha(), [Skeleton(None, self.__window, 5) for i in range(8)]),
            #Map(self.__window, pygame.image.load(GAME_ASSETS["epic_map"]).convert_alpha(), EvilSorceror([self.__window.get_width()/2,self.__window.get_height()/2], self.__window, 10)),
            Map(self.__window, pygame.image.load(GAME_ASSETS["forest_map"]).convert_alpha(), [Skeleton(None, self.__window, 10) for i in range(6)] + [Wraith(None, self.__window, 15 + i) for i in range(3)]),
        ]

    
    # Run game function
    def run(self):
        while True:
            if self.__state == 'menu':  # If the state is 'menu'
                result = self.__menu.run()  # Run the menu and get the result
                self.__current_stage = 0
                self.__game_maps = [ # Resets the list of map classes since they will have been changed from the previous playthrough.
            Map(self.__window, pygame.image.load(GAME_ASSETS["dungeon_map"]).convert_alpha(), [Goblin([50, 50], self.__window, 2), Skeleton([self.__window.get_width() - 120, 50], self.__window, 3)]), 
            Map(self.__window, pygame.image.load(GAME_ASSETS["torture_map"]).convert_alpha(), [Wraith(None, self.__window, 3 + i) for i in range(3)]),
            Map(self.__window, pygame.image.load(GAME_ASSETS["graveyard_map"]).convert_alpha(), [Skeleton(None, self.__window, 5) for i in range(8)]),
            Map(self.__window, pygame.image.load(GAME_ASSETS["epic_map"]).convert_alpha(), [EvilSorceror((self.__window.get_width()/2,self.__window.get_height()/2),self.__window, 10)]),
            Map(self.__window, pygame.image.load(GAME_ASSETS["forest_map"]).convert_alpha(), [Skeleton(None, self.__window, 10) for i in range(6)] + [Wraith(None, self.__window, 15 + i) for i in range(3)]),
            ]
                if result == 'Start Game':  # If the result is 'Start Game'
                    self.__state = 'character_select'  # Change the state to 'character_select'
                elif result == 'Settings':  # If the result is 'Settings'
                    pass  # Settings handling would go here
                elif result == 'Exit':  # If the result is 'Exit'
                    pygame.quit()  # Quit pygame
                    return  # Exit the run method

            elif self.__state == 'character_select':  # If the state is 'character_select'
                selected_character = self.__character_select.run()  # Run the character select screen and get the selected character
                if selected_character == 'back':  # If the selected character is 'back'
                    self.__state = 'menu'  # Change the state to 'menu'
                elif selected_character:  # If a character is selected
                    self.__current_character = selected_character  # Set the current character to the selected character
                    self.__game_maps[self.__current_stage].load_player(selected_character)  # Load the selected character into the game map
                    self.__state = 'game_map'  # Change the state to 'game_map'

            elif self.__state == 'game_map':  # If the state is 'game_map'

                result = self.__game_maps[self.__current_stage].handle_events()  # Handle events in the game map and get the result
                if result == 'back':  # If the result is 'back'
                    self.__state = 'character_select'  # Change the state to 'character_select'
                elif result == 'next':
                    player = self.__game_maps[self.__current_stage].getPlayer() # Take player information from the current stage
                    player_image = self.__game_maps[self.__current_stage].getPlayerImage()

                    self.__current_stage += 1 # Tick up the current stage number

                    self.__game_maps[self.__current_stage].setPlayer(player) # Set the new maps player to the previous one
                    self.__game_maps[self.__current_stage].setPlayerImage(player_image)
                elif result == 'menu':
                    self.__state = 'menu'
                elif result == 'quit':  # If the result is 'quit'
                    pygame.quit()  # Quit pygame
                    return  # Exit the run method
                else:
                    self.__game_maps[self.__current_stage].draw()  # Draw the game map

            for event in pygame.event.get():  # Iterate over the events in the event queue
                if event.type == pygame.QUIT:  # If the event type is QUIT
                    pygame.quit()  # Quit pygame
                    return  # Exit the run method

if __name__ == "__main__":
    game = Game()  # Create an instance of the Game class
    game.run()  # Run the game
