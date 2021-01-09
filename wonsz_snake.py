#!/usr/bin/python3
import pygame
import random
import os



from enum import Enum
from collections import namedtuple
from wonsz_common import *



SNAKE_DENSITY = 30

SNAKE_TEXTURES = list()

def loadAssets():

    snake_path =  os.path.join(ASSETS_PATH ,"snake")

    for i in range(1,7):
        SNAKE_TEXTURES.append(pygame.image.load( os.path.join(snake_path, "head" + str(i) + ".png")) )

    segement_img = pygame.image.load(os.path.join(snake_path, "segment.png"))
    segement_img1 = pygame.image.load(os.path.join(snake_path, "segment1.png"))
    
    SNAKE_TEXTURES.append(segement_img)
    SNAKE_TEXTURES.append(segement_img1)


class MovementDirection(Enum):
    DOWN = 0
    UP = 1
    RIGHT = 2
    LEFT = 3


class SnakeSegment:

    __slots__ = ("pos","direction","inflection", "zez","isDead")
    def __init__(self):
        super().__init__()

        self.pos = Point(100,100)
        self.direction = MovementDirection.RIGHT

        self.inflection = False
        self.zez = Point()
        self.isDead = False


    def updateMovement(self):
        pos = self.pos

        if self.direction == MovementDirection.LEFT:    
            pos.x -= SNAKE_VELOCITY
            if pos.x < -100:
                pos.x += SCREEN_WIDTH + 100

        elif self.direction == MovementDirection.RIGHT:
            pos.x += SNAKE_VELOCITY
            if pos.x > SCREEN_WIDTH+50:
                pos.x -= SCREEN_WIDTH + 100


        elif self.direction == MovementDirection.UP:
            pos.y -= SNAKE_VELOCITY
            if pos.y < -100:
                pos.y += SCREEN_HEIGHT + 100

        elif self.direction == MovementDirection.DOWN:
            pos.y += SNAKE_VELOCITY
            if pos.y > SCREEN_HEIGHT + 50:
                pos.y -= SCREEN_HEIGHT + 100


    def onUpdate(self, previous):
        if previous.inflection and self.zez_reached(previous):

             self.inflection = True
             
             previous.inflection = False

             self.zez.x = previous.zez.x
             self.zez.y = previous.zez.y

             self.alignWithPreviousSegment(previous)

    def zez_reached(self,previous) -> bool:

        if self.direction == MovementDirection.LEFT:
            return self.pos.x <= previous.zez.x

        elif self.direction == MovementDirection.RIGHT:
            return self.pos.x >= previous.zez.x

        elif self.direction == MovementDirection.UP:
            return self.pos.y <= previous.zez.y

        elif self.direction == MovementDirection.DOWN:
            return self.pos.y >= previous.zez.y
        
        
        return False

    def alignWithPreviousSegment(self,previous):

        self.direction = previous.direction
        self.pos.x = previous.pos.x
        self.pos.y = previous.pos.y

        if self.direction == MovementDirection.LEFT:
            self.pos.x += SNAKE_DENSITY
        
        elif self.direction == MovementDirection.RIGHT:
            self.pos.x -= SNAKE_DENSITY

        elif self.direction == MovementDirection.UP:
            self.pos.y += SNAKE_DENSITY

        elif self.direction == MovementDirection.DOWN:
            self.pos.y -= SNAKE_DENSITY


    def render(self, screen):

        image = SNAKE_TEXTURES[7 if self.isDead else 6]
        if self.direction == MovementDirection.LEFT or self.direction == MovementDirection.RIGHT:
            #screen.blit(image, (self.pos.x, self.pos.y + 3))
            screen.blit(image, (self.pos.x - 5, self.pos.y))

        else:
            image = pygame.transform.rotate(image, 90 if self.direction == MovementDirection.UP else -90)
            #screen.blit(image,(self.pos.x + 2 ,self.pos.y))
            screen.blit(image,(self.pos.x , self.pos.y - 5))

    def getRect(self) -> pygame.Rect:

        result = None

        if self.direction == MovementDirection.UP or self.direction == MovementDirection.DOWN:
            result = pygame.Rect(self.pos.x + 6, self.pos.y, 16, 25)

        else:
            result = pygame.Rect(self.pos.x + 1, self.pos.y + 5, 25, 16)

        return result



class SnakeHead(SnakeSegment):

    __slots__ = ("t_anim","costume","next_direction")

    def __init__(self):
        super().__init__()
        self.t_anim = 0
        self.costume = 0
        self.next_direction = None

    def onUpdate(self,previous):

        if not self.inflection:
            keys = pygame.key.get_pressed()

            if self.direction.value < 2:
                if keys[pygame.K_RIGHT]:
                    self.inflection = True
                    self.direction = MovementDirection.RIGHT

                elif keys[pygame.K_LEFT]:
                    self.inflection = True
                    self.direction = MovementDirection.LEFT

                elif self.next_direction is not None:

                    if self.next_direction == MovementDirection.LEFT or self.next_direction == MovementDirection.RIGHT:
                        self.inflection = True
                        self.direction = self.next_direction
                        self.next_direction = None
            else:
                if keys[pygame.K_UP]:
                    self.inflection = True
                    self.direction = MovementDirection.UP
                
                elif keys[pygame.K_DOWN]:
                    self.inflection = True
                    self.direction = MovementDirection.DOWN

                elif self.next_direction is not None:

                    if self.next_direction == MovementDirection.UP or self.next_direction == MovementDirection.DOWN:
                        self.inflection = True
                        self.direction = self.next_direction
                        self.next_direction = None

            if self.inflection:
                self.zez.x = self.pos.x
                self.zez.y = self.pos.y
                #self.zez = self.pos

        if self.t_anim > 10:
            self.t_anim = 0
            self.costume += 1
            self.costume %= 2

        else:
            self.t_anim+=1

    def render(self,screen):

        if self.direction == MovementDirection.RIGHT:
            image = SNAKE_TEXTURES[5 if self.isDead else self.costume]
            screen.blit(image, (self.pos.x - 5, self.pos.y - 4))

        elif self.direction == MovementDirection.LEFT:
            image = SNAKE_TEXTURES[5 if self.isDead else self.costume]
            image = pygame.transform.flip(image,True,False)
            screen.blit(image, (self.pos.x - 19,self.pos.y - 4))

        elif self.direction == MovementDirection.UP:
            index = 4 if self.isDead else self.costume + 2
            screen.blit(SNAKE_TEXTURES[index], (self.pos.x - 2, self.pos.y - (12 if index == 2 else 10)))

        elif self.direction == MovementDirection.DOWN:
            image = SNAKE_TEXTURES[4 if self.isDead else self.costume + 2]
            image = pygame.transform.flip(image,False,True)
            screen.blit(image, (self.pos.x - 2 ,self.pos.y - 5 ))


    def getRect(self) -> pygame.Rect:
        if self.direction == MovementDirection.RIGHT:
            return pygame.Rect(self.pos.x, self.pos.y + 1, 41, 19)

        elif self.direction == MovementDirection.LEFT:
            return pygame.Rect(self.pos.x - 14, self.pos.y + 1, 41, 19)

        elif self.direction == MovementDirection.UP:

            return pygame.Rect(self.pos.x + 3, self.pos.y - 5, 19, 37)

        elif self.direction == MovementDirection.DOWN:

            return pygame.Rect(self.pos.x + 3, self.pos.y, 19, 37)

        return None


class DeadSegmentParticle:
        
    __slots__ = ("segment", "lifetime")
    def __init__(self, segment):
        self.segment = segment
        self.lifetime = random.randint(10,30)
        segment.isDead = True

class Snake:

    __slots__ = ("head", "segmentList","deadSegments")

    def __init__(self):
        self.segmentList = list()
        self.deadSegments = list()

        self.head = SnakeHead()
        self.segmentList.append(self.head)

        for i in range(0,3):
            self.addSegment()


    def onMouseMovement(self, d_x:int,d_y:int):

        if abs(d_x) > abs(d_y) + 30:
            self.head.next_direction = MovementDirection.LEFT if d_x < 0 else MovementDirection.RIGHT

        elif abs(d_y) > abs(d_x) + 30:
            self.head.next_direction = MovementDirection.UP if d_y < 0 else MovementDirection.DOWN

    def onUpdate(self):
        self.segmentList[-1].inflection = False


        i = len(self.segmentList) - 1
        #p1 = self.segmentList[i]
        while i > 0:

            self.segmentList[i].onUpdate(self.segmentList[i-1])
            i-=1


        self.segmentList[0].onUpdate(None)

        for segment in reversed(self.segmentList):
            segment.updateMovement()


        result = False

        i = self.checkInnerCollision()
        if i is not None:
            for j in range(i,len(self.segmentList)):
                #self.segmentList[j].isDead = True

                result = True
                self.deadSegments.append( DeadSegmentParticle(self.segmentList[j]) )

            self.segmentList = self.segmentList[0:i]

        for deadSegment in self.deadSegments:

            deadSegment.lifetime-=1
            if deadSegment.lifetime <= 0:
                self.deadSegments.remove(deadSegment)
                
        return result

    def addSegment(self):
        new_segment = SnakeSegment()
        new_segment.alignWithPreviousSegment( self.segmentList[-1] )

        self.segmentList.append(new_segment)


    def checkInnerCollision(self):

        head_rect = self.segmentList[0].getRect()

        for i in range(3,len(self.segmentList)):

            segment_rect = self.segmentList[i].getRect()

            if segment_rect.colliderect(head_rect):
                return i

        return None

    def __len__(self):
        return len(self.segmentList)


    def render(self,screen):

        for deadSegment in self.deadSegments:
            deadSegment.segment.render(screen)

        for segment in reversed(self.segmentList):
            segment.render(screen)


if __name__ == "__main__":
    print("Snake test")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    loadAssets()

    pygame.display.set_caption("Wonsz1 test")
    snake1 = Snake()
    clock = pygame.time.Clock()



    quit = False
    mouse_pos = (0,0)

    while not quit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit = True

                elif event.key == pygame.K_s:
                    snake1.addSegment()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                mouse_pos = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos1 = pygame.mouse.get_pos()

                d_x = pos1[0] - mouse_pos[0]
                d_y = pos1[1] - mouse_pos[1]

                snake1.onMouseMovement(d_x,d_y)

        snake1.onUpdate()

        screen.fill((0,68,0))
        snake1.render(screen)

        pygame.display.flip()
        clock.tick(60)           

    pygame.quit()
