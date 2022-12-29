#snage game taken from https://www.edureka.co/blog/snake-game-with-pygame/
import pygame
import time
import numpy as np
import random
from math import sqrt
from QTable import QTable

table = QTable()

pygame.init()
 
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
 
dis_width = 600
dis_height = 400
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 50
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def manhattan(a, b):
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))
 
def drawSnake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def getState(x1, y1, snake_list, foodx, foody):
    s = [0] * 6
    #celle occupate dal corpo
    for i in snake_list[:-1]:
        if i == [x1, y1-snake_block]:
            s[QTable.IND_UP] = 1
        if i == [x1+snake_block, y1]:
            s[QTable.IND_RIGHT] = 1
        if i == [x1, y1+snake_block]:
            s[QTable.IND_DOWN] = 1
        if i == [x1-snake_block, y1]:
            s[QTable.IND_LEFT] = 1
    #celle occupate dal muro
    if (y1-snake_block) < 0:
        s[QTable.IND_UP] = 1
    if (x1+snake_block) >= dis_width:
        s[QTable.IND_RIGHT] = 1
    if (y1+snake_block) >= dis_height:
        s[QTable.IND_DOWN] = 1
    if (x1-snake_block) < 0:
        s[QTable.IND_LEFT] = 1
    #posizione mela
    if foodx > x1:
        s[QTable.IND_POS_FOOD_H] = 1
    elif foodx == x1:
        s[QTable.IND_POS_FOOD_H] = 0
    else:
        s[QTable.IND_POS_FOOD_H] = -1
    if foody > y1:
        s[QTable.IND_POS_FOOD_V] = 1
    elif foody == y1:
        s[QTable.IND_POS_FOOD_V] = 0
    else:
        s[QTable.IND_POS_FOOD_V] = -1
    #trasformo in stringa
    return ('%s%s%s%s%s%s' % (s[0],s[1],s[2],s[3],s[4],s[5]))

def getReward(precx1, precy1, x1, y1, snake_list, snake_head, foodx, foody):
    if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
        return -100
    for x in snake_list[:-1]:
        if x == snake_head:
            return -100
    if x1 == foodx and y1 == foody:
        return 20
    return (manhattan([precx1,precy1], [foodx,foody]) - manhattan([x1,y1], [foodx,foody]))/snake_block

def getChangePosition(action):
    y1_change = 0
    x1_change = 0
    if action == QTable.IND_ACTION_UP:
        y1_change = -snake_block
        x1_change = 0
    elif action == QTable.IND_ACTION_RIGHT:
        x1_change = snake_block
        y1_change = 0
    elif action == QTable.IND_ACTION_DOWN:
        y1_change = snake_block
        x1_change = 0
    elif action == QTable.IND_ACTION_LEFT:
        x1_change = -snake_block
        y1_change = 0
    return (x1_change, y1_change)

def gameLoop():
    game_over = False
 
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_list = []
    length_of_snake = 1
 
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
 
    while not game_over:
        precx1 = x1
        precy1 = y1
        state = getState(x1, y1, snake_list, foodx, foody)
        action = table.chooseAction(state)
        x1_change, y1_change = getChangePosition(action)
        #cambiare da schiacciare pulsanti a RL
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT:
            #         x1_change = -snake_block
            #         y1_change = 0
            #     elif event.key == pygame.K_RIGHT:
            #         x1_change = snake_block
            #         y1_change = 0
            #     elif event.key == pygame.K_UP:
            #         y1_change = -snake_block
            #         x1_change = 0
            #     elif event.key == pygame.K_DOWN:
            #         y1_change = snake_block
            #         x1_change = 0
        x1 += x1_change
        y1 += y1_change
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        reward = getReward(precx1, precy1, x1, y1, snake_list, snake_head, foodx, foody)
        temp_x1, temp_y1 = getChangePosition(table.chooseAction(getState(x1, y1, snake_list, foodx, foody)))
        temp_x1 = temp_x1 + x1
        temp_y1 = temp_y1 + y1
        futureReward = getReward(x1, y1, temp_x1, temp_y1, snake_list, snake_head, foodx, foody)
        table.updateTable(state, action, reward, futureReward)
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            gameLoop()
        for x in snake_list[:-1]:
            if x == snake_head:
                gameLoop()
        if len(snake_list) > length_of_snake:
            del snake_list[0]
        
        dis.fill(white)
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        drawSnake(snake_block, snake_list)
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()

gameLoop()