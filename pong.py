#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 19:46:44 2022

@author: InfinityCoding
"""

# =============================================================================
# Import reqirements
# =============================================================================

import pygame, sys, random

# =============================================================================
# Initial Variables
# =============================================================================

FACTOR = 1
WIDTH = 960 * FACTOR
HEIGTH = 540 * FACTOR
FPS = 60
GAMEOVER = False
PAUSE = True 
WINNER = None
WINS = [0, 0] # List where the Wins will saved (idx0 = left, idx1 = right)
 
# =============================================================================
# Pygame Set-Up
# =============================================================================

pygame.init()
pygame.display.set_caption("Ping Pong")
screen = pygame.display.set_mode( (WIDTH, HEIGTH) )
clock = pygame.time.Clock()
pygame.mouse.set_visible(False) # Hide Mouse while Playing

# =============================================================================
# Creating a Class for the punchers
# =============================================================================

class punch(pygame.sprite.Sprite):
    def __init__(self, side, FACTOR):
        super().__init__()
        self.FACTOR = FACTOR
        self.image = pygame.Surface([5*self.FACTOR, 60*self.FACTOR]) # Puncher
        self.image.fill((255, 255, 255)) # Change Color of Puncher to white
        self.rect = self.image.get_rect()
        self.side = side
        if self.side == "left":
            self.pos = [10*self.FACTOR, HEIGTH//2]
            self.rect.center = self.pos
        else:
            self.pos = [WIDTH-10*self.FACTOR, HEIGTH//2]
            self.rect.center = self.pos
            
    def key_input(self):
        """Checking Keyboard-Input and change if necessary the Position of the Puncher"""
        keys = pygame.key.get_pressed()
        if self.side == "right": # if right Puncher
            if keys[pygame.K_UP] and self.pos[1] > 30*self.FACTOR: # if Arrow-Up pressed and Windowborder not reached
                self.pos = [self.pos[0], self.pos[1]-10*self.FACTOR]
            if keys[pygame.K_DOWN] and self.pos[1] < HEIGTH-30*self.FACTOR: # if Arrow-Down pressed and Windowborder not reached
                self.pos = [self.pos[0], self.pos[1]+10*self.FACTOR]
        else: # if right Puncher
            if keys[pygame.K_w] and self.pos[1] > 30*self.FACTOR: # if W pressed (Up) and Windowborder not reached
                self.pos = [self.pos[0], self.pos[1]-10*self.FACTOR]
            if keys[pygame.K_s] and self.pos[1] < HEIGTH-30*self.FACTOR: # if S pressed (Down) and Windowborder not reached
                self.pos = [self.pos[0], self.pos[1]+10*self.FACTOR]
            
    def reset(self):
        if self.side == "left":
            self.pos = [10*self.FACTOR, HEIGTH//2]
            self.rect.center = self.pos
        else:
            self.pos = [WIDTH-10*self.FACTOR, HEIGTH//2]
            self.rect.center = self.pos
                
    def update(self):
        self.key_input()
        self.rect.center = self.pos
        
# =============================================================================
# Creating a Class for the Ball
# =============================================================================

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ball.png").convert_alpha() # load Image
        self.rect = self.image.get_rect() # Get rect of the Image, to move it
        self.rect.center = (WIDTH//2, HEIGTH//2) # set position to the Window-center
        self.direction = pygame.math.Vector2(self.createDirection(), self.createDirection()) # create random 2d-Vector 
        self.speed = FACTOR # customize Speed, std is 1, if you want speed up the Ball, change the value
    
    def checkDirection(self):
        global GAMEOVER, WINNER
        if self.rect.bottom >= HEIGTH or self.rect.top <= 0: # if the Ball reached top or bottom border of the Window
            self.direction.y = -self.direction.y # invert y-Direction
        if self.rect.right >= WIDTH or self.rect.left <= 0: # if the Ball reched the right or left border -> GameOver
            GAMEOVER = True 
            WINNER = "right" if self.direction.x < 0 else "left"
            WINS[0] += 1 if WINNER == "left" else WINS[0]
            WINS[1] += 1 if WINNER == "right" else WINS[1]
            pygame.mouse.set_visible(True) # show Mouse
        
    def createDirection(self):
        # function to generate a random direction: -5 < direction < -2 < 2 <direction < 5
        direction = (random.randint(2, 5), random.randint(-5, -2))
        direction = random.choice(direction)
        return direction
    
    def reset(self):
        self.rect.center = (WIDTH//2, HEIGTH//2) # set position to the Window-center
        self.direction = pygame.math.Vector2(self.createDirection(), self.createDirection()) # create random 2d-Vector 

    def update(self):
        self.checkDirection() # check if ball reached one of the Window-Borders
        self.rect.x += self.direction.x * self.speed # move ball at the x-Postion with a distance of Vector.x * speed
        self.rect.y += self.direction.y * self.speed # move ball at the y-Postion with a distance of Vector.y * speed
        if pygame.sprite.spritecollide(ball, punchers, False): # if Ball collide with a Puncher
            # first we have to set the Position of the rect correctly, beacause, if the puncher
            # hits the Ball with a corner or the top/bottom the Ball bugs in the puncher
            if self.direction.x < 0: # if moving to the left
                self.rect.left = 10*FACTOR + 5*FACTOR/2
            else:
                self.rect.right = WIDTH - (10*FACTOR + 5*FACTOR/2)
            self.direction.x = -self.direction.x # invert the x-Direction
            
# =============================================================================
# define a Function for render messages
# =============================================================================
            
def debug(info, pos=(10, 10), text_size = 10, centered=False, offset = 0): # Function for render Infos
    font = pygame.font.SysFont("liberationserif", text_size)    
    text = font.render(str(info), True, (255, 255, 255))
    if centered:
        center = [WIDTH//2-text.get_width()//2, HEIGTH//2-text.get_height()//2]
        center[1] += text.get_height()*offset
        pos = center
    screen.blit(text, pos)
    pygame.display.update()


# =============================================================================
# Setting up the elements and variables
# =============================================================================

# Creating Instances and Sprites
left_punch = punch("left", FACTOR) # define an new Instance of the punch-Class for creating the left puncher
right_punch = punch("right", FACTOR) # define an new Instance of the punch-Class for creating the right puncher
ball = Ball() # define an new Instance of the Ball-Class for creating the Ball

# creating the two Sprite-Groups
punchers = pygame.sprite.Group() 
ball_sprite = pygame.sprite.Group()

# adding the Elements to the Sprite-Groups
punchers.add(left_punch)
punchers.add(right_punch)
ball_sprite.add(ball)

debug("Press space to start!", text_size=50, centered = True)
                    

# =============================================================================
# Starting main Game Loop
# =============================================================================

while True:   
    for event in pygame.event.get(): # cheking for events
        if event.type == pygame.QUIT: # if teh user close the Window
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if PAUSE:
                    PAUSE = False
                    pygame.mouse.set_visible(False)
                elif GAMEOVER:
                    ball.reset()
                    left_punch.reset()
                    right_punch.reset()
                    GAMEOVER = False
                    PAUSE = True
                    screen.fill("black")
                    debug("Press space to start!", text_size=50, centered=True)
                else:
                    screen.fill("black")
                    debug("Paused!", text_size=50, centered=True, offset = -0.5)
                    debug("Press space to continue.", text_size=50, centered=True, offset = 0.5)
                    PAUSE = True
                    pygame.mouse.set_visible(True)
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    if GAMEOVER == False:
        if PAUSE == False:
            screen.fill('black')
            # update and draw the Sprite Groups, if it isn't paused
            punchers.update()
            ball_sprite.update()
            punchers.draw(screen)
            ball_sprite.draw(screen)
            # Render the Framerate
            debug(str(round(clock.get_fps()))+" fps")
        # update the whole Screen
        pygame.display.update()
        clock.tick(FPS)        

    elif GAMEOVER == True:
        screen.fill("black")
        debug("The %s player scored!" % WINNER, text_size=50, centered=True, offset = -0.5) # Scoring text
        debug("Press space to continue!") # Scoring text
        debug("%s" % WINS, text_size=50, centered=True, offset = 0.5) # Scoring text
        
        clock.tick(1)
