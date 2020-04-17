# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time     : 2020/4/15 8:26
# @Author   : yangrui
"""
from sys import exit
from edit import TextBox
from eight import *
from pygame.locals import *
import pygame

firstcell = None
loc = -1
init_list = []
def get_result(src):
    result = []
    result.append(DFS(src))
    result.append(BFS(src))
    result.append(BFS_W(src))
    result.append(BFS_P(src))
    result.append(BFS_S(src))
    return result

def init():
    global init_list
    over_list = ['00.png','01.png','02.png','03.png','04.png','05.png','06.png','07.png','08.png']
    init_list = generator()
    print(init_list)
    cellist = []
    global loc
    for i in range(3):
        for j in range(3):
            if init_list[3*i+j] == 0:
                loc = 3*i+j
                print(loc)
            game_img = pygame.image.load(over_list[init_list[3*i+j]]).convert()
            print(over_list[init_list[3*i+j]])
            cellist.append(game_img)
            screen.blit(game_img, (206+130*j,7+130*i))
    return cellist, loc

def switch(cellist, pos1, pos2):
    if pos1>-1 and pos1<9 and pos2>-1 and pos2<9:
        screen.blit(cellist[pos1], (206 + 130 * (pos2 % 3), 7 + 130 * (pos2 // 3)))
        screen.blit(cellist[pos2], (206 + 130 * (pos1 % 3), 7 + 130 * (pos1 // 3)))
        cellist[pos1], cellist[pos2] = cellist[pos2], cellist[pos1]
        init_list[pos1], init_list[pos2] = init_list[pos2], init_list[pos1]
        pygame.display.update()

def pos(x, y):
    i = (x - 206)//130
    j = (y - 7)//130
    if i>-1 and i<3 and j>-1 and j<3:
        return 3*j+i
    return -1


def play(event, cellist):
    global firstcell
    global loc
    if event.type == MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        if x>640 and x<753 and y>150 and y<200:
            cu, eu, path = BFS_S(init_list)
            if path[0] == 'r':
                switch(cellist, loc, loc+1)
                loc = loc+1
            elif path[0] == 'l':
                switch(cellist, loc, loc - 1)
                loc = loc - 1
            elif path[0] == 'd':
                switch(cellist, loc, loc + 3)
                loc = loc + 3
            else:
                switch(cellist, loc, loc - 3)
                loc = loc - 3
        else:
            p = pos(x, y)
            print("dibeijidna",p)
            if p==-1:
                return -1
            if firstcell is None:
                firstcell = p
            else:
                print(loc, firstcell, p)
                if loc in [firstcell, p] and firstcell in [p-3, p-1, p+1, p+3]:
                    switch(cellist, firstcell, p)
                    loc = p if firstcell==loc else firstcell
                firstcell = None
        if init_list == [1, 2, 3, 8, 0, 4, 7, 6, 5]:
            return 1
    return 0

pygame.init()
screen = pygame.display.set_mode((800, 406), 0, 32)
pygame.display.set_caption("实验")

bg = pygame.image.load("0.png").convert()
screen.blit(bg,(0,0))

def data(result):
    my_font = pygame.font.Font("simsun.ttc", 32)
    table = pygame.image.load("3.png").convert()
    screen.blit(table, (168,97,613,280))
    for i in range(5):
        text1 = my_font.render(str(result[i][0]), True, (0,0,0))
        text2 = my_font.render(str(result[i][1]), True, (0, 0, 0))
        screen.blit(text1, (520-text1.get_width()/2, 172+42*i))
        screen.blit(text2, (700-text2.get_width()/2, 172+42*i))

edit = TextBox((310, 30, 200, 50))
def get_click(event, state):
    if event.type == MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        print(x,y)
        if x>21 and x<136 and y>65 and y<115:
            bg = pygame.image.load("1.png").convert()
            screen.blit(bg, (0, 0))
            edit.blink = True
            edit.buffer = ['']
            edit.get_event(event)
            edit.update()
            edit.draw(screen)
            pygame.display.update()
            return 1
        elif x>21 and x<136 and y>150 and y<203:
            bg = pygame.image.load("2.png").convert()
            screen.blit(bg, (0, 0))
            pygame.display.update()
            return 2
        elif x>21 and x<136 and y>235 and y<290:
            pass
        elif x>21 and x<136 and y>325 and y<375:
            pygame.quit()
            exit()
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()
    return state

def test():
    x, y = pygame.mouse.get_pos()
    print(x, y)
    if x > 660 and x < 758 and y > 30 and y < 77:
        src = []
        print(edit.buffer)
        for i in edit.buffer:
            if i:
                src.append(eval(i))
        if sovle(src):
            data(get_result(src))
    elif x>525 and x<640 and y>30 and y<78:
        edit.buffer = [str(x) for x in generator()]
        edit.update()
        edit.draw(screen)

def game(event,state):
    global loc
    if event.type == MOUSEBUTTONUP:
        x, y = pygame.mouse.get_pos()
        if x > 623 and x < 772 and y > 39 and y < 90:
            cellist, loc = init()
            return cellist, loc, 3

    return [], -1, state
def work():
    state = 0
    cellist = []
    while True:
        for event in pygame.event.get():
            if state == 0:
                state = get_click(event, state)
            elif state == 1:
                edit.get_event(event)
                edit.update()
                edit.draw(screen)
                pygame.display.update()
                state = get_click(event, state)
                if event.type == MOUSEBUTTONDOWN:
                    test()
            elif state == 2:
                state = get_click(event, state)
                cellist, loc, state = game(event, state)
            elif state == 3:
                state = get_click(event, state)
                game(event, state)
                flag = play(event, cellist)
                if flag == 0:
                    break
                elif flag ==1:
                    bg = pygame.image.load("4.png").convert()
                    screen.blit(bg, (206, 7))
                    state = 2
                else:
                    pass
        pygame.display.update()

if __name__ == '__main__':
    work()