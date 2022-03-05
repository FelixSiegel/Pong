#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 19:46:44 2022

@author: felix
"""

import pygame, sys, random

# Initial Variables
FACTOR = 1
WIDTH = 960 * FACTOR
HEIGTH = 540 * FACTOR
FPS = 60
GAMEOVER = False
PAUSE = True 
WINNER = None

# Pygame Set-Up
pygame.init()
pygame.display.set_caption("Ping Pong")
screen = pygame.display.set_mode( (WIDTH, HEIGTH) )
clock = pygame.time.Clock()
pygame.mouse.set_visible(False) # Hide Mouse while Playing


class punch(pygame.sprite.Sprite):
    def __init__(self, side, FACTOR):
        super().__init__()
        self.image = pygame.Surface([5*FACTOR, 60*FACTOR]) # Puncher
        self.image.fill((255, 255, 255)) # Change Color of Puncher to white
        self.rect = self.image.get_rect()
        self.side = side
        if self.side == "left":
            self.pos = [10*FACTOR, HEIGTH//2]
            self.rect.center = self.pos
        else:
            self.pos = [WIDTH-10*FACTOR, HEIGTH//2]
            self.rect.center = self.pos
            
    def key_input(self):
        """Checking Keyboard-Input and change if necessary the Position of the Puncher"""
        keys = pygame.key.get_pressed()
        if self.side == "right": # if right Puncher
            if keys[pygame.K_UP] and self.pos[1] > 30*FACTOR: # if Arrow-Up pressed and Windowborder not reached
                self.pos = [self.pos[0], self.pos[1]-10*FACTOR]
            if keys[pygame.K_DOWN] and self.pos[1] < HEIGTH-30*FACTOR: # if Arrow-Down pressed and Windowborder not reached
                self.pos = [self.pos[0], self.pos[1]+10*FACTOR]
        else: # if right Puncher
            if keys[pygame.K_w] and self.pos[1] > 30*FACTOR: # if W pressed (Up) and Windowborder not reached
                self.pos = [self.pos[0], self.pos[1]-10*FACTOR]
            if keys[pygame.K_s] and self.pos[1] < HEIGTH-30*FACTOR: # if S pressed (Down) and Windowborder not reached
                self.pos = [self.pos[0], self.pos[1]+10*FACTOR]
                
    def update(self):
        self.key_input()
        self.rect.center = self.pos

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
            pygame.mouse.set_visible(True) # show Mouse
        
    def createDirection(self):
        # function to generate a random direction: -5 < direction < -2 < 2 <direction < 5
        direction = (random.randint(2, 5), random.randint(-5, -2))
        direction = random.choice(direction)
        return direction

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
                self.rect.right = WIDTH*FACTOR - (10*FACTOR + 5*FACTOR/2)
            self.direction.x = -self.direction.x # invert the x-Direction
            
def debug(info, pos=(10, 10)): # Function for render Infos
    font = pygame.font.SysFont("dejavusansmono", 10)    
    text = font.render(str(info), True, (255, 255, 255))
    screen.blit(text, pos)


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

screen.fill('black')
font = pygame.font.SysFont("liberationserif", 50*FACTOR)
message_Pause = font.render("Paused! Press space to continue.", True, (255, 255, 255)) # Game Over Text
screen.blit(message_Pause, (WIDTH//2-message_Pause.get_width()//2, HEIGTH//2-message_Pause.get_height()//2))
                    

# main Game Loop
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
                else:
                    screen.fill('black')
                    font = pygame.font.SysFont("liberationserif", 50*FACTOR)
                    message_Pause = font.render("Paused! Press space to continue.", True, (255, 255, 255)) # Game Over Text
                    screen.blit(message_Pause, (WIDTH//2-message_Pause.get_width()//2, HEIGTH//2-message_Pause.get_height()//2))
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

    if GAMEOVER == True:
        screen.fill('black')
        # creating a Game Over and Winner Text
        font = pygame.font.SysFont("liberationserif", 50*FACTOR)
        message_GO = font.render("Game Over!", True, (255, 255, 255)) # Game Over Text
        message_WN = font.render("The %s player winns!" % WINNER, True, (255, 255, 255)) # Winner Text
        # add the messages to the screen
        screen.blit(message_GO, (WIDTH//2-message_GO.get_width()//2, HEIGTH//2-message_GO.get_height()))
        screen.blit(message_WN, (WIDTH//2-message_WN.get_width()//2, HEIGTH//2))
        # update the Screen
        pygame.display.update()
        # needs to run further untill the user triggerd the QUIT-Event
        clock.tick(1)
