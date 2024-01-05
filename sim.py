import pygame
import random
import numpy as np
import copy
from network import Network

pygame.init()

WIDTH, HEIGHT = 1024,1024
DENSITY = 0.04
FACTOR = 8
FPS = 60
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREENISH = (15,255,45)



screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def randombool(randratio):
    return random.random() <= randratio

class Cell():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.net = Network(8,2,8)
    
    def draw(self):
        pygame.draw.rect(screen,(GREENISH),pygame.Rect((self.x)*FACTOR,(self.y)*FACTOR,FACTOR,FACTOR))

    def moveRight(self, world):
        if self.x+1 < len(world[0]):
            try:
                if world[self.y][self.x+1] is None:
                    world[self.y][self.x+1], world[self.y][self.x] = self, None
                    self.x+=1
            except:
                print(self.x,self.y,len(world[0]),len(world))
                raise "moveRight"
        else:
            self.moveRandom(world)
                

    def moveLeft(self, world):
        if self.x > 0:
            try:
                if world[self.y][self.x-1] is None:
                    world[self.y][self.x-1], world[self.y][self.x] = self, None
                    self.x-=1
            except:
                print(self.x,self.y,len(world[0]),len(world))
                raise "moveLeft"
        else:
            self.moveRandom(world)
            
    def moveDown(self, world):
        if self.y+1 < len(world):
            try:
                if world[self.y+1][self.x] is None:
                    world[self.y+1][self.x], world[self.y][self.x] = self, None
                    self.y+=1
            except:
                print(self.x,self.y,len(world[0]),len(world))
                raise "moveDown"
        else:
            self.moveRandom(world)
                
    def moveUp(self, world):
        if self.y > 0:
            try:
                if world[self.y-1][self.x] is None:
                    world[self.y-1][self.x], world[self.y][self.x] = self, None
                    self.y-=1
            except:
                print(self.x,self.y,len(world[0]),len(world))
                raise "moveUp"
        else:
            self.moveRandom(world)
            
    def moveTopRight(self, world):
        if self.x+1 < len(world[0]) and self.y > 0:
            try:
                if world[self.y-1][self.x+1] is None:
                    world[self.y-1][self.x+1], world[self.y][self.x] = self, None
                    self.x+=1
                    self.y-=1
            except:
                print(self.x,self.y,len(world[0]),len(world))
                raise "moveTopRight"
        else:
            self.moveRandom(world)
        
    def moveTopLeft(self, world):
        if self.x > 0 and self.y > 0:
            try:
                if world[self.y-1][self.x-1] is None:
                    world[self.y-1][self.x-1], world[self.y][self.x] = self, None
                    self.x-=1
                    self.y-=1
            except:
                print(self.x,self.y,len(world[0]),len(world))
                raise "moveTopLeft"
        else:
            self.moveRandom(world)


    def moveBottomRight(self, world):
        if self.x+1 < len(world[0]) and self.y+1 < len(world):
            try:
                if world[self.y+1][self.x+1] is None:
                    world[self.y+1][self.x+1], world[self.y][self.x] = self, None
                    self.x+=1
                    self.y+=1
            except:
                print(self.x,self.y,len(world[0]),len(world))
                raise "moveBottomRight"
        else:
            self.moveRandom(world)
        
    def moveBottomLeft(self, world):
        if self.x > 0 and self.y+1 < len(world):
            try:
                if world[self.y+1][self.x-1] is None:
                    world[self.y+1][self.x-1], world[self.y][self.x] = self, None
                    self.x-=1
                    self.y+=1
            except:
                print(self.x,self.y,len(world[0]),len(world))
                raise "moveBottomLeft"
        else:
            self.moveRandom(world)

    def moveRandom(self, world):
        random.choice([self.moveRight,self.moveLeft,self.moveUp,self.moveDown,self.moveTopRight,self.moveTopLeft,self.moveBottomRight,self.moveBottomLeft])(world)
        
                
    def move(self, world):
        fnclist = [self.moveRight,self.moveLeft,self.moveUp,self.moveDown,self.moveTopRight,self.moveTopLeft,self.moveBottomRight,self.moveBottomLeft]
        output_vector = self.net.move(self.fetchParameters(world))
        if sum(output_vector) != 0:
            fnclist[np.argmax(output_vector)](world)

    def fetchParameters(self,world):
        offset = [(x,y) for x in (0,-1,1) for y in (0,-1,1)][1:]
        parameters = list()
        for x in offset:
            if 0 <= self.x+x[0] < len(world[0]) and 0 <= self.y+x[1] < len(world):
                if world[self.x + x[0]][self.y + x[1]] is None:
                    parameters.append(0)
                else:
                    parameters.append(1)
            else:
                parameters.append(0)
        
        return parameters  


class World:
    def __init__(self):
        self.world = ([[Cell(x,y) if randombool(DENSITY) else None for x in range(WIDTH//FACTOR)] for y in range(HEIGHT//FACTOR)])
            


    def draw(self):
        coords = [(x,y) for x in range(WIDTH//FACTOR) for y in range(HEIGHT//FACTOR)]
        random.shuffle(coords)
        for y in coords:
            cell = self.world[y[1]][y[0]]
            if cell:
                cell.draw() 
                cell.moveRandom(self.world) #Random Movement
                #cell.move(self.world) #Neural Movement (Doesnt work Right now)
        
                    
running = True


new_world = World()
print(len(new_world.world))
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    new_world.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()