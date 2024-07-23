import pygame
from assets import GAME_ASSETS
import time
from textWriter import TextRenderer
from button import Button

class Combat:
    # Attributes
    __enemy = None
    __player = None
    __map_image = None
    __window = None
    __player_image = None
    __enemy_image = None
    __console_writer = None
    __acknowledged_button = None  # Adding the new attribute

    def __init__(self, player, enemy, window, player_image):
        self.__enemy = enemy
        self.__player = player
        self.__window = window
        print(self.__window.get_size())
        self.__map_image = pygame.image.load(GAME_ASSETS["arena"]).convert_alpha()
        self.__map_image = pygame.transform.scale(self.__map_image, (self.__window.get_width(), self.__window.get_height())) # Rescale map image
        self.__player_image = pygame.transform.scale(player_image, (100, 150)) # Rescale player image
        self.__enemy_image = pygame.transform.scale(self.__enemy.getImage(), (100, 150)) # Rescale enemy image
        self.__console_writer = TextRenderer(window, pygame.Rect(310, 70, 210, 500), 26) # make a TextRenderer object for writing in the background place
        self.__acknowledged_button = Button(400, 400, 200, 40, (0,150,0), 28, "Acknowledged?", "acknowledge")

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

    def getConsoleWriter(self):
        return self.__console_writer

    def getAcknowledgedButton(self):
        return self.__acknowledged_button

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

    def setConsoleWriter(self, newConsoleWriter):
        self.__console_writer = newConsoleWriter

    def setAcknowledgedButton(self, newAcknowledgedButton):
        self.__acknowledged_button = newAcknowledgedButton

    #Behaviours
    # checks whether user is ready to continue battle
    def seek_acknowledgement(self):
        while not self.acknowledgement():
                self.__acknowledged_button.draw(self.__window)
                pygame.display.flip()
        
        # Reset the arena
        self.__window.fill((0, 0, 0))  # Clear the console
        self.draw_arena()  # Draw the arena

    # Throws user into a loop of turn-based battle to the death
    def enter_battle(self):

        player = self.getPlayer()
        enemy = self.getEnemy()

        while player.isAlive() and enemy.isAlive():  # Repeats combat loop until either party dies

            chosen_attack = self.choose_attack() # Allows player to enter a key input to choose a certain attack
            output = player.attack(enemy, chosen_attack)  # Player takes action
            self.__console_writer.display_output(output) # Writes every item stored in output onto the screen
            pygame.display.flip()
            
            self.seek_acknowledgement()

            if not enemy.isAlive():  # Checks whether the enemy has died
                message = []
                message.append(f"{enemy.getName()} has been killed.")
                message.append(f"{player.getName()} has gained {enemy.getXpValue()} experience points!")
                
                if player.leveled_up:
                    message.append("Congratulations on leveling up! Time to allocate some skill points!")
                    player.setCurrentHP(player.getMaxHP()) # Fully heal the player on level ups

                self.__console_writer.display_output(message)
                pygame.display.flip()
                self.seek_acknowledgement()

                player = player.gain_experience(enemy.getXpValue()) # Upates the upgraded player with newly assigned stats after level ups

                return player  # Return the updated player information to wherever 'combat' was called

            output = player.upkeepPhase()  # Counts a turn to have passed, triggering all regeneration and ticking up all status effect timers
            self.__console_writer.display_output(output)
            pygame.display.flip()

            self.seek_acknowledgement()

            output = enemy.attack(player)  # Enemy takes action
            self.__console_writer.display_output(output) # Enemy action's outputs are displayed
            pygame.display.flip()
            
            self.seek_acknowledgement()

            self.__window.fill((0, 0, 0))  # Clear the console again for player's turn
            self.draw_arena()  # Draw the arena again

            while not player.isAlive():
                self.__window.blit(pygame.transform.scale(pygame.image.load(GAME_ASSETS["lose_screen"]).convert_alpha(), (800, 600)), (0, 0))
                pygame.display.flip()


    def draw_arena(self):
        window = self.getWindow()

        #load images
        window.blit(self.__map_image, (0, 0))
        window.blit(self.__player_image, (150, (window.get_height() - self.__player_image.get_height()) / 2))
        window.blit(self.__enemy_image, (650, (window.get_height() - self.__enemy_image.get_height()) / 2))
        
        #player information
        self.__player.listAttacks(window, pygame.Rect(8, 420, 110, 200), 12)
        stat_writer = TextRenderer(window, pygame.Rect(8, 210, 110, 200), 12) # Creates an instance of text renderer to write stats in the stat area
        stat_list = []
        for stat, value in self.__player.getStats().items():
            stat_list.append(f"{stat}: {value}")
        stat_writer.display_output(stat_list)

        #enemy information

        pygame.display.flip() #update the display

    def choose_attack(self):
        chosen_attack = None
        self.__console_writer.display_output(["Enter the number of the desired attack."])
        pygame.display.flip()

        while not chosen_attack: # Repeats a loop checking for key inputs until an attack is chosen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        chosen_attack = 1
                    elif event.key == pygame.K_2:
                        chosen_attack = 2
                    elif event.key == pygame.K_3:
                        chosen_attack = 3
                    elif event.key == pygame.K_4:
                        chosen_attack = 4
                    elif event.key == pygame.K_5:
                        chosen_attack = 5

        self.__window.fill((0, 0, 0))  # Clear the console for the enemy's turn
        self.draw_arena()  # Redraw the arena

        return chosen_attack # Returns chosen attack number

    def acknowledgement(self):
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = event.pos
                        return self.__acknowledged_button.is_clicked(pos)  