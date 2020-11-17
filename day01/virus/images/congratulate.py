# coding:utf-8
import pygame, sys, os, easygui, random, time
from pygame.locals import *
pygame.init()
# 设置一个长宽窗口
canvas = pygame.display.set_mode((480, 660))
canvas.fill([255, 255, 255])
c = pygame.image.load('images/c.png')

class Con():
    def __init__(self,x,y,xx):
        self.x = x
        self.y = y
        self.xx = xx
    def paint(self):
        canvas.blit(c,(self.x,self.y))
    def step(self):
        self.y += 4
        self.x += self.xx
cons = []
  
def isTime(lastTime,interval):
    if lastTime == 0:
        return True
    currentTime = time.time()
    return currentTime - lastTime >= interval
lastTime = 0
interval = 0.25    
def add():
    global lastTime
    if not isTime(lastTime, interval):
        return
    lastTime = time.time()
    x = random.randint(0,480-56)
    y = -52
    xx = random.uniform(-0.35,0.35)
    con = Con(x,y,xx)
    if len(cons) <= 20:
        cons.append(con)
    
    
def congratulate(): 
    add()
    for c in cons:
        c.paint()
        c.step()
    
 
