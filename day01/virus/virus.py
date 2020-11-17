# coding:utf-8
import pygame, time, random, sys, os
from pygame.locals import *
pygame.init()

# 创建窗口
can = pygame.display.set_mode((480, 660))
can.fill((255, 255, 255))

# 设置窗口标题
pygame.display.set_caption("消灭病毒") 

# 加载图片
bg0 = pygame.image.load("images/bg.png")  # 背景图片
bg1 = pygame.image.load("images/bg_1.png")  # 背景图片
bg2 = pygame.image.load("images/bg_4.png")  # 背景图片
bg3 = pygame.image.load("images/bg_3.png")  # 背景图片
blast = pygame.image.load("images/blast01.png")  # 爆炸图片
bullet0 = pygame.image.load("images/bullet.png")  # 子弹图片
bullet1 = pygame.image.load("images/bullet_2.png")  # 子弹图片
bullet2 = pygame.image.load("images/zhenguan.png")  # 子弹图片
bullet3 = pygame.image.load("images/yinghua.png")  # 子弹图片
diamond = pygame.image.load("images/diamond.png")  # 钻石图片
double_bullet = pygame.image.load("images/double_bullet.png")  # 多排子弹图片
gold_coin = pygame.image.load("images/gold_coin.png")  # 金币数量图片
blue = pygame.image.load("images/blue.png")  # 金币背景图片
gold = pygame.image.load("images/gold.png")  # 金币图片
logo = pygame.image.load("images/logo.png")  # logo图片
plane0 = pygame.image.load("images/plane.png")  # 飞机图片
plane1 = pygame.image.load("images/plane_4.png")  # 飞机图片
plane2 = pygame.image.load("images/plane_2.png")  # 飞机图片
plane3 = pygame.image.load("images/plane_3.png")  # 飞机图片                                   
virus_green = pygame.image.load("images/virus_green.png")  # 绿病毒图片
virus_red = pygame.image.load("images/virus_red.png")  # 红病毒图片
virus_yellow = pygame.image.load("images/virus_yellow.png")  # 黄病毒图片

class Canvas():
    def blit(self,img,*point):
        x = point[-1]
        y = point[0]
        can.blit(img,(x,y))
        if img == bg0 or img == bg1 or img == bg2 or img == bg3:
            can.blit(img,(GameVar.x2,GameVar.y2))
canvas = Canvas()


#事件控制方法
def handleEvent():
    for event in pygame.event.get():#循环遍历事件
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        # 点击鼠标左键控制游戏开始到运行状态
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if  GameVar.state == 'START':
                GameVar.state = 'RUNNING' 
        if event.type == KEYDOWN and event.key == K_SPACE and GameVar.state == 'GAME_OVER':
            pygame.quit()
            os.system(sys.executable + ' virus.py')
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            # 运行状态下，控制飞机跟随鼠标移动
            if GameVar.state == 'RUNNING':
                GameVar.plane.x = event.pos[0] - GameVar.plane.width / 2
                GameVar.plane.y = event.pos[1] - GameVar.plane.height / 2
            # 鼠标移出移入事件控制运行和暂停状态切换
            if isMouseOut(event.pos[0], event.pos[1]):
                if  GameVar.state == 'RUNNING':
                    GameVar.state = 'PAUSE'
            if isMouseOver(event.pos[0], event.pos[1]):
                if  GameVar.state == 'PAUSE':
                    GameVar.state = 'RUNNING'  
                                          
# 判断时间间隔方法
def isActionTime(lastTime, interval):
    if lastTime == 0:
        return True
    currentTime = time.time()
    return currentTime - lastTime >= interval
    
# 写文字方法
def renderText(text, position, center, size):#（文字，坐标，坐标是否在中心，大小）
    # 设置字体样式和大小
    my_font = pygame.font.Font('images/msyh.ttf', size)
    text = my_font.render(text, True, (255, 255, 255))
    if center:
        textRect = text.get_rect()  # 获得要显示的文本的rect
        textRect.center = position  # 设置显示文本的坐标中心点
        can.blit(text, textRect)
    else:
        can.blit(text, position)
  
# 判断鼠标是否移出画布
def isMouseOut(x, y):
    if x >= 479 or x <= 0 or y >= 659 or y <= 0:
        return True

# 判断鼠标是否移入画布
def isMouseOver(x, y):
    if x > 0 and x < 479 and y > 0 and y < 659:
        return True
        
# 定义Sky类
class Sky():
    def __init__(self):
        self.width = 480
        self.height = 660
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = -self.height
    def paint(self):
        canvas.blit(bg0, (self.x1, self.y1))
    def step(self):
        self.y1 = self.y1 + 0.5
        GameVar.y2 = GameVar.y2 + 0.5
        if self.y1 > self.height:
            self.y1 = -self.height
        if GameVar.y2 > self.height:
            GameVar.y2 = -self.height
            
# 定义父类FlyingObject
class FlyingObject():
    def __init__(self, x, y, width, height, life, img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.life = life
        self.img = img
        self.lastTime = 0
        self.interval = 0.01
        self.canDelete = False
    # 碰撞检测方法
    def hit(self, object):
        o = object
        return o.x > self.x - o.width and o.x < self.x + self.width and o.y > self.y - o.height and o.y < self.y + self.height
    # 对象之间碰撞后的处理
    def bang(self, bangsign,component):
        # 病毒或双排子弹和飞机碰撞之后的处理
        if bangsign:
            self.canDelete = True
            if bangsign == 2:
                self.life -= 1
            if bangsign == 3:
               GameVar.canDouble = True
               GameVar.doubleTime += 30
        # 病毒和子弹碰撞之后的处理
        else:   
            if hasattr(self, 'coin'):#判断为病毒          
                self.life -= component.life
            if not hasattr(self, 'coin'):#判断为子弹
                self.life -= self.life    
            if self.life <= 0:
                self.canDelete = True
                if not hasattr(self, 'coin'):#判断为子弹
                    can.blit(blast, (self.x, self.y - 50))                 
                if hasattr(self, 'coin'):#判断为病毒
                    GameVar.coin += self.coin      
    # 越界处理
    def outOfBounds(self):
        return self.y > 660
    
# 定义Bullet类
class Bullet(FlyingObject):
    def __init__(self, x, y, width, height, life, img):
        FlyingObject.__init__(self, x, y, width, height, life, img)
    def paint(self):
        canvas.blit(bullet0,(self.x,self.y))
    # 重写step方法
    def step(self):        
        self.y = self.y - 9
    # 重写判断是否越界的方法
    def outOfBounds(self):
        return self.y < -self.height
    def setPower(self,life):
        self.life  = life
      
# 定义Virus类
class Virus(FlyingObject):
    def __init__(self, x, y, width, height, type, life, coin, img, perX, perY, size, degree, perDegree):
        FlyingObject.__init__(self, x, y, width, height, life, img)
        self.x = random.randint(0, 480 - self.width)
        self.y = -self.height
        self.perX = perX
        self.perY = perY
        self.size = size
        self.type = type
        self.coin = coin 
        self.degree = degree
        self.perDegree = perDegree
    def setLife(self,life):
        self.life  = life
    def paint(self):
        if self.degree == 360:
            self.perDegree = -5
        elif self.degree == 0:
            self.perDegree = 5
        self.degree += self.perDegree
        orig_rect = self.img.get_rect()
        rot_image = pygame.transform.rotate(self.img, self.degree)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        can.blit(rot_image, (self.x, self.y))  
        renderText(str(self.life), (self.x + (self.width / 2), self.y + (self.height / 2)), True, self.size)
    def step(self):
        # 判断是否到了移动的时间间隔
        if not isActionTime(self.lastTime, self.interval):
            return
        self.lastTime = time.time()
        # 控制移动速度
        self.y = self.y + self.perY
        self.x = self.x + self.perX
        if self.x < 0 or self.x > 480 - self.width:
            self.perX = -self.perX
     
# 定义Plane类
class Plane(FlyingObject):
    def __init__(self, x, y, width, height, life, img):
        FlyingObject.__init__(self, x, y, width, height, life, img)
        self.width = 100
        self.height = 120
        self.x = 190
        self.y = 495
        # 射击时间间隔
        self.shootLastTime = 0
        self.shootInterval = 0.14
    def paint(self):
        canvas.blit(plane0, (self.x, self.y))
    def shoot(self):
        if not isActionTime(self.shootLastTime, self.shootInterval):
            return
        self.shootLastTime = time.time()
        if GameVar.canDouble == True:
            plane01 = Bullet(self.x + self.width / 2, self.y - 25, 10, 29, 1, bullet0)
            plane01.setPower(1)
            GameVar.bullets.append(plane01)
            plane02 = Bullet(self.x + self.width / 2 - 10, self.y - 25, 10, 29, 1, bullet0)
            plane02.setPower(1)
            GameVar.bullets.append(plane02)
            GameVar.doubleTime = GameVar.doubleTime - 1
            if GameVar.doubleTime == 0:
                GameVar.canDouble = False
        else:
            plane03 = Bullet(self.x + self.width / 2 - 5, self.y - 25, 10, 29, 1, bullet0)
            plane03.setPower(1)
            GameVar.bullets.append(plane03)
            
# 定义Double类
class Double(FlyingObject):
    def __init__(self, x, y, width, height, life, img, perX, perY):
        FlyingObject.__init__(self, x, y, width, height, life, img)
        self.x = random.randint(0, 480 - self.width)
        self.y = -self.height
        self.perX = perX
        self.perY = perY
    def paint(self):
        can.blit(self.img, (self.x, self.y))
    def step(self):
        if not isActionTime(self.lastTime, self.interval):
            return
        self.lastTime = time.time()
        # 控制移动速度
        self.y += self.perY
        self.x += self.perX
        if self.x < 0:
            self.perX = 2
        if self.x > 480 - self.width:
            self.perX = -2
        
def objectEnter():
    # 控制产生病毒的间隔
    if not isActionTime(GameVar.lastTime, GameVar.interval):
        return
    GameVar.lastTime = time.time()
    # 随机生成坐标
    x = random.randint(0, 480 - 50)
    x1 = random.randint(0, 480 - 60)
    x2 = random.randint(0, 480 - 140)
    x3 = random.randint(0, 480 - 50)
    perX = random.randint(-2, 4) # x变化幅度
    perY = random.randint(2, 3) # y的变化幅度
    n = random.randint(0, 9)  # 根据随机整数的值生成不同的病毒
    m = random.randint(0, 15)  # 随机生成双排子弹
    if n <= 6:
        yellowVirus = Virus(x, 0, 50, 50, 1, 8, 10, virus_yellow, perX, perY, 20, 0, 1)
        yellowVirus.setLife(8)
        GameVar.viruses.append(yellowVirus)
    elif n == 8 or n == 7:
        redVirus = Virus(x1, 0, 68, 68, 2, 18, 50, virus_red,perX, perY, 25, 0, 1)
        redVirus.setLife(18)
        GameVar.viruses.append(redVirus)
    elif n == 9:
        if len(GameVar.viruses) == 0 or GameVar.viruses[0].type != 3:
            greenVirus = Virus(x2, 0, 150, 150, 3, 88, 100, virus_green,perX, 0.5, 55, 0, 1)
            greenVirus.setLife(88)
            GameVar.viruses.insert(0, greenVirus)
    if m == 10:
        GameVar.doubleBullets.append(Double(x3, 0, 50, 50, 1, double_bullet, perX, perY))    
# 画出游戏中的对象
def paintObject():    
    # 控制对象绘制的时间间隔
    if not isActionTime(GameVar.paintLastTime, GameVar.paintInterval):
        return
    GameVar.paintLastTime = time.time()
    GameVar.sky.paint()
    for Virus in GameVar.viruses:
        Virus.paint()
    for doubleBullet in GameVar.doubleBullets:
        doubleBullet.paint()
    GameVar.plane.paint()
    for bullet in GameVar.bullets:
        bullet.paint()
    # 画出并写出金币数和战力值
    can.blit(gold_coin, (15, 15))
    can.blit(diamond, (377, 15))
    renderText(str(GameVar.coin), (50, 15), False, 20)
    renderText(str(GameVar.planes), (420, 15), False, 20)
    
# 游戏中对象移动的方法
def objectStep():
    GameVar.sky.step()
    for Virus in GameVar.viruses:
        Virus.step()
    for doubleBullet in GameVar.doubleBullets:
        doubleBullet.step()
    for bullet in GameVar.bullets:
        bullet.step()
    
# 检测对象之间发生碰撞的方法
def checkHit():
    # 检测每个病毒是否与飞机发生碰撞
    for Virus in GameVar.viruses:
        if GameVar.plane.hit(Virus):
            Virus.bang(1,GameVar.plane)
            GameVar.plane.bang(2,Virus)
        # 检测每颗子弹是否与病毒发生碰撞
        for bullet in GameVar.bullets:
            if Virus.hit(bullet):
                Virus.bang(0,bullet)
                bullet.bang(0,Virus)
    # 检测飞机是否与双排子弹碰撞
    for doubleBullet in GameVar.doubleBullets:
        if GameVar.plane.hit(doubleBullet):
            doubleBullet.bang(3,GameVar.plane)

#删除对象
def deleteObject():
    for Virus in GameVar.viruses:
        if Virus.canDelete or Virus.outOfBounds():
            GameVar.viruses.remove(Virus)
    for bullet in GameVar.bullets:
        if bullet.canDelete or bullet.outOfBounds():
            GameVar.bullets.remove(bullet)
    for doubleBullet in GameVar.doubleBullets:
        if doubleBullet.canDelete or doubleBullet.outOfBounds():
            GameVar.doubleBullets.remove(doubleBullet)
    if GameVar.plane.canDelete == True:
        GameVar.planes -= 1
        if GameVar.planes <= 0:
            GameVar.state = 'GAME_OVER'
        else:
            GameVar.plane = Plane(0, 0, 100, 120, 1, plane0)
    
# 创建游戏变量
class GameVar():
    sky = None
    plane = None
    viruses = []
    bullets = []
    doubleBullets = []
    canDouble = False
    doubleTime = 0   #双排子弹时间
    startText = 240  # 文字初始坐标
    overText = 240
    lastTime = 0
    interval = 2
    paintLastTime = 0
    paintInterval = 0
    coin = 0
    planes = 3
    state = 'START'
    scale = 22  #设置呼吸金币大小
    moveText = 1 # 游戏开始和结束文字动画控制
    moveImage = 1 #游戏开始和结束图片动画控制
    x2 = 0
    y2 = -660
    
# 创建sky对象
GameVar.sky = Sky()
# 创建飞机对象
GameVar.plane = Plane(0, 0, 100, 120, 1, plane0)

# 游戏状态控制
def contralState():
    if  GameVar.state == 'START':
        GameVar.sky.paint()
        GameVar.startText += GameVar.moveText
        renderText('移 动 消 灭 病 毒', (GameVar.startText, 380), True, 25)
        if GameVar.startText == 250:
            GameVar.moveText = -1
        if GameVar.startText == 230:
            GameVar.moveText = 1   
        can.blit(logo, (50, 100))
        GameVar.plane.paint()
        GameVar.plane.y += GameVar.moveImage
        if GameVar.plane.y == 495:
            GameVar.moveImage = 1
        if GameVar.plane.y == 515:
            GameVar.moveImage = -1
        pygame.display.update() 
    elif GameVar.state == 'RUNNING':
        objectEnter()
        paintObject()
        objectStep()
        GameVar.plane.shoot()
        checkHit()
        deleteObject()
    elif GameVar.state == 'PAUSE':
        paintObject()
    elif GameVar.state == 'GAME_OVER':
        GameVar.sky.paint()
        can.blit(logo, (50, 100))
        can.blit(blue, (130, 410))
        renderText('你 赚 到 了 :', (GameVar.overText, 350), True, 25)
        GameVar.overText += GameVar.moveText
        if GameVar.overText == 250:
            GameVar.moveText = -1
        if GameVar.overText == 230:
            GameVar.moveText = 1
        renderText('x   ' + str(GameVar.coin), (265, 440), True, 25)
        # 添加呼吸金币
        rotatedSurf = pygame.transform.scale(gold, (GameVar.scale, GameVar.scale))
        rot_rect = rotatedSurf.get_rect()
        rot_rect.center = (190, 442)
        can.blit(rotatedSurf, rot_rect)
        if GameVar.scale == 20:
            GameVar.moveImage = 1
        elif GameVar.scale == 35:
            GameVar.moveImage = -1
        GameVar.scale += GameVar.moveImage
       
while True:
    # 游戏状态控制
    contralState()
    # 更新屏幕内容
    pygame.display.update()
    # 监听有没有按下退出按钮
    handleEvent()
    # 等待0.01秒后再进行下一次循环
    time.sleep(0.008)
