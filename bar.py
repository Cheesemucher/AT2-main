import pygame

class Bar:
    __previous_width = None
    __window = None
    __entity = None
    __maxStat = None
    __barLength = None
    __maxtolengthRatio = None
    __pos = None
    __stat = None
    __colour = None

    def __init__(self, window, entity, pos, stat):
        self.__stat = stat
        self.__window = window
        self.__entity = entity
        self.__maxStat = self.getMaxStat() 
        self.__barLength = window.get_width() / 4
        self.__maxtolengthRatio = self.__maxStat / self.__barLength # How much max stat should be represented by one bar length

        self.__pos = pos

        # Set the colour based on the stat
        if stat == "HP":
            self.__colour = (255, 0, 0)  # Red for HP
        elif stat == "Stamina":
            self.__colour = (255, 255, 0)  # Yellow for Stamina
        elif stat == "Mana":
            self.__colour = (0, 0, 255)  # Blue for Mana
        else:
            self.__colour = (0, 255, 0)  # Default to green for other stats

    # Accessors
    def getPreviousWidth(self):
        return self.__previous_width

    def getCurrentStat(self):
        method_name = f"getCurrent{self.__stat}"  # Construct the method name
        current_stat_method = getattr(self.__entity, method_name)  # Get the method
        return current_stat_method()  # Call the method to get the current value

    def getMaxStat(self):
        method_name = f"getMax{self.__stat}"  # Construct the method name
        current_stat_method = getattr(self.__entity, method_name)  # Get the method
        return current_stat_method()  # Call the method to get the current value

    def getBarLength(self):
        return self.__barLength

    def getMaxtolengthRatio(self):
        return self.__maxStat / self.__barLength

    # Mutators
    def setPreviousWidth(self, newWidth):
        self.__previous_width = newWidth

    def setMaxStat(self, newMaxStat):
        self.__maxStat = newMaxStat

    def setBarLength(self, newBarLength):
        self.__barLength = newBarLength

    def update_quantity(self):
        # Get the width of the bar based upon current stat values and ratio of max stat to bar size (in pixels)
        current_width = min(self.getCurrentStat() / self.getMaxtolengthRatio(), self.getBarLength())
        
        # Draw the background of the bar
        pygame.draw.rect(self.__window, (0, 0, 0), (self.__pos[0], self.__pos[1], self.getBarLength(), 25))

        # Draw the current bar
        pygame.draw.rect(self.__window, self.__colour, (self.__pos[0], self.__pos[1], current_width, 25))
        
        # Draw the border of the bar
        pygame.draw.rect(self.__window, (255, 255, 255), (self.__pos[0], self.__pos[1], self.getBarLength(), 25), 4)



