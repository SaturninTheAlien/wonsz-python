#!/usr/bin/python3
import pygame


SNAKE_VELOCITY = 4

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800


ASSETS_PATH = "assets/"


class Point:
    __slots__ = ("x", "y")
    def __init__(self, x=0,y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "(x:"+str(self.x)+", y:"+str(self.y)+")"

    def __getitem__(self,index):
        return self.__getattribute__(self.__slots__[index])

    def __setitem__(self,index, value):
        return self.__setattr__(self.__slots__[index], value)


class TextInFrame():

    __slots__ = "fillColor", "borderColor", "strokeWidth", "font", "fontColor", "_surface", "_content"
    def __init__(self,strokeWidth,fillColor,borderColor, font,fontColor):

        self._content = None
        self._surface = None

        self.fillColor = fillColor
        self.borderColor = borderColor
        self.strokeWidth = strokeWidth

        self.font =font
        self.fontColor = fontColor

    def updateContent(self, text:str):

        self._content = self.font.render(text,1,self.fontColor)
        
        self._surface = pygame.Surface((self._content.get_width() + 40, self._content.get_height() + 40))
        self._surface.fill(self.fillColor)

        if len(self.fillColor) == 4:
            self._surface.set_alpha(self.fillColor[3])
        
    def render(self, screen, pos_x, pos_y):

        #self._surface.draw(pos_x,pos_y)

        screen.blit(self._surface, (pos_x,pos_y))

        var1 = self._content.get_width() + 40
        var2 = self._content.get_height() + 40 - self.strokeWidth

        pygame.draw.rect(screen, self.borderColor, (pos_x,pos_y, var1, self.strokeWidth ))
        pygame.draw.rect(screen, self.borderColor, (pos_x,pos_y + self.strokeWidth, self.strokeWidth, var2))
        pygame.draw.rect(screen, self.borderColor, (pos_x + var1 - self.strokeWidth, pos_y+self.strokeWidth, self.strokeWidth, var2))
        pygame.draw.rect(screen, self.borderColor, (pos_x+self.strokeWidth , pos_y+var2,  var1 - 2*self.strokeWidth, self.strokeWidth))

        screen.blit(self._content, (pos_x+20,pos_y+20))