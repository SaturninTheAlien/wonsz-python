#!/usr/bin/python3
import pygame
import random
import os
import math

from wonsz_common import *

APPLE_TEXTURES = list()


def loadAssets():
    apple_dir = os.path.join(ASSETS_PATH,"apple")


    for file in os.listdir(apple_dir):
        n = len(file)
        if n > 3 and file[n-4 : n] == ".png":
            APPLE_TEXTURES.append(pygame.image.load(os.path.join(apple_dir,file)))


class Apple:

    __slots__ = ("pos", "texture", "origPosY", "angle1")
    def __init__(self, pos_x,pos_y):

        self.pos = Point(pos_x,pos_y)
        self.origPosY = pos_y
        self.angle1 = 0

        self.texture = random.choice(APPLE_TEXTURES)

    def onUpdate(self, snake):

        self.angle1 += 0.025
        if self.angle1 > 2*math.pi:
            self.angle1 -= 2*math.pi

        self.pos.y = self.origPosY + 10*math.sin(self.angle1)

        r1 = pygame.Rect(self.pos.x+5,self.pos.y+5, self.texture.get_width() - 10, self.texture.get_height() - 10)
        if r1.colliderect(snake.head.getRect()):
            return 1


    def render(self, screen):
        screen.blit(self.texture, (self.pos.x, self.pos.y))


if __name__ == "__main__":
    print("Snake apple test")
    #loadAssets()