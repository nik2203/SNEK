from os import close
import pygame
import time
import random


pygame.init()
width,height=800,600#screen
disp=pygame.display.set_mode((width,height))
pygame.display.set_caption("SNEK")
green,red,black,white,grey=(0,204,153),(255,8,0),(0,0,0),(255,255,255),(128,128,128)
font_style=pygame.font.SysFont(None,30)
cell=20
level_no=1
pygame.mixer.init()
food= pygame.mixer.Sound('apple_bite.mp3')
death = pygame.mixer.Sound('oof.mp3')
fh=open('scores.txt','r')
scores=fh.read().split('\n')
hs=max(scores)
fh.close()

def get_food_position(width, height, body):
    while True:
        food_x=round(random.randrange(0,width-cell)/cell)*cell
        food_y=round(random.randrange(0,height-cell)/cell)*cell

        if [food_x, food_y] not in body:
            return food_x, food_y

def gameloop():
    end=0
    x,y,x1,y1=width/2,height/2,0,0#x,y->head pos;x1,y1->change in pos
    snake_speed=10
    body,blen=[],1
    clk=pygame.time.Clock()
    food_x, food_y= get_food_position(width,height, body)
    while not end:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                end=1
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    x1,y1=-cell,0
                elif event.key==pygame.K_UP:
                    x1,y1=-0,-cell
                elif event.key==pygame.K_RIGHT:
                    x1,y1=cell,0
                elif event.key==pygame.K_DOWN:
                    x1,y1=0,cell
        x+=x1;y+=y1
        if x>width or x<0 or y>height or y<0:#screen boundary condition
            pygame.mixer.Sound.play(death)
            break
        disp.fill(black)
        pygame.draw.rect(disp,red,[food_x,food_y,cell,cell])
        head=[]
        head.append(x);head.append(y)
        body.append(head)#append new head to body
        for block in body[:blen-1]:
            if block==head:#snake head touches body
                end=1
        if len(body)>blen:#snake movement display
            del body[0]
        for block in body:
            pygame.draw.rect(disp,green,[block[0],block[1],cell,cell])
        score=font_style.render("Score: "+str(blen-1),True,white)
        snk_sp=font_style.render("Snake Speed: "+str(snake_speed),True,white)
        lvl=font_style.render("Current Level:"+str(level_no),True,white)
        disp.blit(score,[25,0])
        disp.blit(snk_sp,[25,20])
        disp.blit(lvl,[625,0])
        pygame.display.update()
        if food_x==x and food_y==y:#contact with food
            food_x, food_y= get_food_position(width,height, body)
            blen+=1#body length increases
            pygame.mixer.Sound.play(food)
            if snake_speed<60:
                snake_speed+=0.5
        clk.tick(snake_speed)#fps
    clk.tick(snake_speed)
    disp.fill(black)
    m=font_style.render("Game Over",True,red)
    disp.blit(m,[(width/2)-40,height/2])
    f_score=font_style.render("Score: "+str(blen-1),True,white)
    h_score=font_style.render("High Score: "+str(hs),True,white)
    disp.blit(f_score,[(width/2)-30,(height/2)+27])
    disp.blit(h_score,[(width/2)-45,(height/2)+54])
    fh=open('scores.txt','a')
    fh.write('\n'+str(blen-1))
    fh.close()
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit()
gameloop()