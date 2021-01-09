#!/usr/bin/python3
import pygame
import random

import wonsz_snake
import wonsz_apple


from wonsz_common import *





class Wonsz1App:
    def __init__(self):

        wonsz_snake.loadAssets()
        wonsz_apple.loadAssets()

        self.snake = wonsz_snake.Snake()
        self.apple = None #wonsz_apple.Apple(100,100)
        self.apple_respawn_time = 0


        self.font = pygame.font.Font(None, SCREEN_WIDTH // 24)

        self.score_gui = TextInFrame(5,(0,0,255,128),(255,0,0,128),self.font,(255,255,0,255) )
        self.updateScore()

        self.showGUI = True

    def render(self,screen):

        screen.fill((0,68,0))

        self.snake.render(screen)
        if self.apple is not None:  self.apple.render(screen)


        if self.showGUI: 
            self.score_gui.render(screen,21,21)

    def findNewPositionForApple(self):
        
        pos_x = random.randint(100, SCREEN_WIDTH  - 100)
        pos_y = random.randint(100, SCREEN_HEIGHT - 100)

        return (pos_x,pos_y)


    def updateScore(self):
        self.score_gui.updateContent("Length: "+str(len(self.snake)))

    def onUpdate(self):

        if self.snake.onUpdate():
            self.updateScore()

        

        if self.apple is None:
            
            if self.apple_respawn_time <=0:
                self.apple = wonsz_apple.Apple(*self.findNewPositionForApple())

            else:
                self.apple_respawn_time-=1
                
        elif self.apple.onUpdate(self.snake) == 1:
            
            self.snake.addSegment()
            self.apple = None
            self.apple_respawn_time = random.randint(30,120)
            self.updateScore()

def main():
    
    print("Wonsz1 python version")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    pygame.display.set_caption("Wonsz1")
    clock = pygame.time.Clock()
    game = Wonsz1App()

    quit = False
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit = True
                elif event.key == pygame.K_F1:
                    game.showGUI = not game.showGUI


        game.onUpdate()
        game.render(screen)

        pygame.display.flip()
        clock.tick(60)           

    pygame.quit()



if __name__ == "__main__":
    main()
