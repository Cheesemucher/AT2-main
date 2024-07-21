import pygame

class Button:
    # Attributes
    __button_area = None
    __colour = None
    __original_colour = None
    __hover_colour = None
    __text = None
    __font = None
    __text_surface = None
    __text_rect = None
    __value = None 
    # End attributes

    def __init__(self, x, y, width, height, colour, text, value):
        self.__button_area = pygame.Rect(x, y, width, height)
        self.__colour = colour
        self.__original_colour = colour
        self.__hover_colour = tuple(max(0, c - 50) for c in colour)
        self.__text = text
        self.__font = pygame.font.Font(None, 36)
        self.__text_surface = self.__font.render(self.__text, True, (255, 255, 255))
        self.__text_rect = self.__text_surface.get_rect(center=self.__button_area.center)
        self.__value = value 

    # Accessors
    def getButtonArea(self):
        return self.__button_area

    def getColour(self):
        return self.__colour

    def getOriginalColour(self):
        return self.__original_colour

    def getHoverColour(self):
        return self.__hover_colour

    def getText(self):
        return self.__text

    def getFont(self):
        return self.__font

    def getTextSurface(self):
        return self.__text_surface

    def getTextRect(self):
        return self.__text_rect

    def getValue(self): 
        return self.__value

    # Mutators
    def setButtonArea(self, newButtonarea):
        self.__button_area = newButtonarea

    def setColour(self, newColour):
        self.__colour = newColour

    def setOriginalColour(self, newOriginalcolour):
        self.__original_colour = newOriginalcolour

    def setHoverColour(self, newHovercolour):
        self.__hover_colour = newHovercolour

    def setText(self, newText):
        self.__text = newText

    def setFont(self, newFont):
        self.__font = newFont

    def setTextSurface(self, newTextsurface):
        self.__text_surface = newTextsurface

    def setTextRect(self, newTextrect):
        self.__text_rect = newTextrect

    def setValue(self, newValue):  
        self.__value = newValue

    # Behaviors
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()  # track cursor position to update the button when hovering over it

        if self.getButtonArea().collidepoint(mouse_pos):  # Change button colour if mouse is over it
            self.setColour(self.getHoverColour())
        else:
            self.setColour(self.getOriginalColour())

        pygame.draw.rect(screen, self.getColour(), self.getButtonArea())
        screen.blit(self.getTextSurface(), self.getTextRect())

    def is_clicked(self, pos):
        return self.getButtonArea().collidepoint(pos)
