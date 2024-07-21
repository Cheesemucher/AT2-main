import pygame
import time
from button import Button

class SkillPointsAllocator:
    #attributes
    __character = None
    __available_points = None
    __width = None
    __height = None
    __screen = None
    __font = None
    __exit_button = None
    __stats = None
    __buttons = None
    __attribute_upgrades = None
    #end attributes

    def __init__(self, character):
        self.__character = character
        self.__available_points = 0
        self.__width = 800
        self.__height = 600
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        pygame.font.init()
        self.__font = pygame.font.Font(None, 36)
        self.__exit_button = Button(690, 550, 100, 40, (0, 240, 0), 36, "Confirm", "exit")
        self.__stats = []
        self.__buttons = []
        self.__attribute_upgrades = {
            "Strength": lambda: self.__character.setStrength(self.__character.getStrength() + 2), # lambda is used here only to prevent python from checking whether the character has a certain function until it is called,
            "Max Stamina": lambda: self.__character.setMaxStamina(self.__character.getMaxStamina() + 2), # this is necessary as not all characters have all the funcions within this dictionary.
            "Max Mana": lambda: self.__character.setMaxMana(self.__character.getMaxMana() + 10),
            "Max HP": lambda: self.__character.setMaxHP(self.__character.getMaxHP() + 10),
            "Magic Power": lambda: self.__character.setMagicPower(self.__character.getMagicPower() + 2),
            "Magic Resistance Multiplier": lambda: self.__character.setMagicResistance(self.__character.getMagicResistance() - 0.02),
            "Defense Multiplier": lambda: self.__character.setDefenseMultiplier(self.__character.getDefenseMultiplier() - 0.02),
        }

    # Accessors
    def getCharacter(self):
        return self.__character

    def getAvailablePoints(self):
        return self.__available_points

    def getScreen(self):
        return self.__screen

    def getFont(self):
        return self.__font

    def getExitButton(self):
        return self.__exit_button

    def getStats(self):
        return self.__stats

    def getButtons(self):
        return self.__buttons

    def getAttributeUpgrades(self):
        return self.__attribute_upgrades

    # Mutators
    def setCharacter(self, character):
        self.__character = character

    def setAvailablePoints(self, points):
        self.__available_points = points

    def setScreen(self, screen):
        self.__screen = screen

    def setFont(self, font):
        self.__font = font

    def setExitButton(self, button):
        self.__exit_button = button

    def setStats(self, stats):
        self.__stats = stats

    def setButtons(self, buttons):
        self.__buttons = buttons

    def setAttributeUpgrades(self, upgrades):
        self.__attribute_upgrades = upgrades

    # Behaviors
    def draw_text(self, text, x, y, color=(0, 0, 0)):
        text_surface = self.__font.render(text, True, color)
        self.__screen.blit(text_surface, (x, y))

    def draw_buttons(self):
        self.__stats.clear()  # Reset stat list
        self.__buttons.clear()  # Reset button list

        # Create list of stats and their respective buttons
        position_y = 100
        for stat, value in self.__character.getStats().items():
            if "Current" not in stat and "Regen" not in stat:  # The getStats() dictionary has some values which are not to be used here
                self.__stats.append((stat, value, 90, position_y))  # Write a stat and existing value
                button = Button(50, position_y, 30, 30, (0, 255, 0), 36, "+", stat)  # Add a "+" button next to it with the same y position
                self.__buttons.append(button)
                position_y += 50

        self.draw_text(f"Skill Points: {self.__available_points}", 50, 50)

        for stat in self.__stats:
            self.draw_text(f"{stat[0]}: {stat[1]}", stat[2], stat[3])  # Write all relevant character stats

        for button in self.__buttons:
            button.draw(self.__screen)  # Draw the corresponding buttons

    def handle_click(self, pos):
        for button in self.__buttons:
            if button.is_clicked(pos):
                if self.__available_points > 0 and button.getValue() in self.__attribute_upgrades:
                    self.__attribute_upgrades[button.getValue()]()  # Call the lambda function
                    self.__available_points -= 1
                break  # Exit the loop after a single button is found to be clicked

        self.draw_buttons()  # Redraw the screen to update values

    def distribute_points(self, character, available_points):
        self.setCharacter(character)
        self.setAvailablePoints(available_points)

        while self.__available_points > 0:
            self.__screen.fill((255, 255, 255))
            self.draw_buttons()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    self.handle_click(pos)

        # Grey out all buttons after all skill points are spent
        for button in self.__buttons:
            button.setHoverColour((64, 64, 64))
            button.setOriginalColour((128, 128, 128))

        self.__buttons.append(self.__exit_button)  # Add exit button after all points are spent

        while self.__available_points < 1:
            self.__screen.fill((255, 255, 255))
            for stat in self.__stats:
                self.draw_text(f"{stat[0]}: {stat[1]}", stat[2], stat[3])  # Write all relevant character stats

            for button in self.__buttons:
                button.draw(self.__screen)  # Draw the corresponding buttons

            self.draw_text("Out of skill points!", 50, 50)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if self.__exit_button.is_clicked(pos):
                        return self.__character



