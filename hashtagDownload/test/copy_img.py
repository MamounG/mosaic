#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')

black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
crashed = False
carImg = pygame.image.load('hashtag_pictures/42158152_325254711595667_6853004724064702112_n.jpg')


def car(x, y):
    gameDisplay.blit(carImg, (x, y))

while not crashed:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print('Forward')
            elif event.key == pygame.K_ESCAPE:
                print('Backward')
            elif event.key == pygame.K_0:
                crashed = True



    gameDisplay.fill(white)
    car(0, 0)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()