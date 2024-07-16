import pygame
from menu import MainMenu
from character_select import CharacterSelect
from map import Map
from assets import load_assets, GAME_ASSETS

class Game:
    # Attributes
    __window = None  # the 'window' that the game will be displayed on
    __menu = None  # main menu
    __character_select = None  # character selection
    __game_map = None  # actual map for the game
    __state = None  # which state the game is actually in (e.g., menu, character select, etc.)
    __current_character = None  # To store the chosen character

    # End attributes

    def __init__(self):
        pygame.init()
        load_assets()  # load the game image assets
        self.__window = pygame.display.set_mode((800, 600))
        self.__menu = MainMenu(self.__window)  # Create an instance of the MainMenu class
        self.__character_select = CharacterSelect(self.__window)  # Create an instance of the CharacterSelect class
        self.__game_map = Map(self.__window)  # Create an instance of the Map class
        self.__state = 'menu'  # Set the initial state to 'menu'
    
    # Accessors
    def get_window(self):
        return self.__window

    def get_menu(self):
        return self.__menu

    def get_character_select(self):
        return self.__character_select

    def get_game_map(self):
        return self.__game_map

    def get_state(self):
        return self.__state

    def get_current_character(self):
        return self.__current_character

    # Mutators
    def set_window(self, new_window):
        self.__window = new_window

    def set_menu(self, new_menu):
        self.__menu = new_menu

    def set_character_select(self, new_character_select):
        self.__character_select = new_character_select

    def set_game_map(self, new_game_map):
        self.__game_map = new_game_map

    def set_state(self, new_state):
        self.__state = new_state

    def set_current_character(self, new_current_character):
        self.__current_character = new_current_character
    
    # Run game function
    def run(self):
        while True:
            if self.__state == 'menu':  # If the state is 'menu'
                result = self.__menu.run()  # Run the menu and get the result
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
                    self.__game_map.load_player(selected_character)  # Load the selected character into the game map
                    self.__state = 'game_map'  # Change the state to 'game_map'

            elif self.__state == 'game_map':  # If the state is 'game_map'
                result = self.__game_map.handle_events()  # Handle events in the game map and get the result
                if result == 'back':  # If the result is 'back'
                    self.__state = 'character_select'  # Change the state to 'character_select'
                elif result == 'quit':  # If the result is 'quit'
                    pygame.quit()  # Quit pygame
                    return  # Exit the run method
                else:
                    self.__game_map.draw()  # Draw the game map

            for event in pygame.event.get():  # Iterate over the events in the event queue
                if event.type == pygame.QUIT:  # If the event type is QUIT
                    pygame.quit()  # Quit pygame
                    return  # Exit the run method

if __name__ == "__main__":
    game = Game()  # Create an instance of the Game class
    game.run()  # Run the game
