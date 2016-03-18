import pygame
import gameEngine
from pygame.locals import *
import random

pygame.mixer.init

pygame.init

#起始界面的选择器（小坦克）
class Car_Choose(gameEngine.SuperSprite):

    #小坦克选择器的初始化
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("tank_1.gif")
        self.setBoundAction(self.STOP)
        self.setPosition((300, 340))
        self.setAngle(0)

    #点击J射击，选择对应的项（play或者exit）
    def checkEvents(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_j]:
            if self.scene.bulletMyTank.x < 0 and self.scene.bulletMyTank.y < 0:
                self.scene.bulletMyTank.fire()
                self.scene.sound_attack_begin.play()


# 起始界面选择器的炮弹
class Bullet_My_Tank(gameEngine.SuperSprite):

    #炮弹初始化
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("bullet.gif")
        self.imageMaster = pygame.transform.scale(self.imageMaster, (5, 5))
        self.setBoundAction(self.HIDE)
        self.reset()
        self.is_inScreen = False

    #父类函数重写
    def checkEvents(self):
        self.checkBounds()

    #开火
    def fire(self):
        self.setPosition((self.scene.car.x, self.scene.car.y))
        self.setSpeed(12)
        self.setAngle(self.scene.car.rotation)

    #重置
    def reset(self):
        self.setPosition((-100, -100))
        self.setSpeed(0)

#起始界面
class Intro(gameEngine.Scene):

    #起始界面初始化
    def __init__(self):
        gameEngine.Scene.__init__(self)
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = pygame.image.load("Intro_bg.png")

        #坦克和炮弹的实例化
        self.car = Car_Choose(self)
        self.bulletMyTank = Bullet_My_Tank(self)
        self.bulletMyTank.setSpeed(1)
        self.choosePosition = "Play"

        #增加标签
        self.addLabels()
        self.sprites = [self.label_play, self.label_exit, self.car, self.bulletMyTank]

        #声音
        self.sound_choose = pygame.mixer.Sound("bo.wav")
        self.sound_attack_begin = pygame.mixer.Sound("attack_begin.wav")
        self.sound_be_attacked = pygame.mixer.Sound("be_attacked.wav")

        #flag标志位
        self.is_gameTime = False
        self.bugCorrect = 0


    #事件监听器
    def doEvents(self, event):
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_w:
                if self.choosePosition == "Exit":
                    self.choosePosition = "Play"
                    self.sound_choose.play()
                    self.car.setPosition((300, 340))
                    self.car.setAngle(0)
                elif self.choosePosition == "Play":
                    self.choosePosition = "Exit"
                    self.sound_choose.play()
                    self.car.setPosition((300, 400))
                    self.car.setAngle(0)
                
            if event.key == pygame.K_s:
                if self.choosePosition == "Play":
                    self.choosePosition = "Exit"
                    self.sound_choose.play()
                    self.car.setPosition((300, 400))
                    self.car.setAngle(0)
                elif self.choosePosition == "Exit":
                    self.choosePosition = "Play"
                    self.sound_choose.play()
                    self.car.setPosition((300, 340))
                    self.car.setAngle(0)

    #刷新
    def update(self):
        if self.bugCorrect == 1:
            
            choosePlay = self.bulletMyTank.collidesWith(self.label_play)
            if choosePlay == True:
                self.keepGoing = False
                self.is_gameTime = True
                
            chooseExit = self.bulletMyTank.collidesWith(self.label_exit)
            if chooseExit == True:
                self.keepGoing = False

        if self.bugCorrect == 0:
            self.bugCorrect += 1
    

    def addLabels(self):
        #添加play标签
        self.label_play = gameEngine.MultiLabel()
        self.label_play.bgColor = (0, 0, 0)
        self.label_play.fgColor = (255, 255, 255)
        self.label_play.font = pygame.font.SysFont("None", 35)
        self.label_play.size = (60, 60)
        self.label_play.center = (440, 360)
        self.label_play.textLines = ["Play"]

        #添加exit标签
        self.label_exit = gameEngine.MultiLabel()
        self.label_exit.bgColor = (0, 0, 0)
        self.label_exit.fgColor = (255, 255, 255)
        self.label_exit.font = pygame.font.SysFont("None", 35)
        self.label_exit.size = (60, 60)
        self.label_exit.center = (440, 420)
        self.label_exit.textLines = ["Exit"]


#增加Game界面的墙壁
class Wall(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("wall.gif")
        

#Game界面中我方坦克
class My_Tank(gameEngine.SuperSprite):

    #初始化
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("tank_1.gif")
        self.setPosition((100, 500))
        self.setAngle(90)
        self.setBoundAction(self.STOP)

    #事件监听器，只有四个方向可以操作，固定前进速率为3， 同时不能越过边界
    def checkEvents(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.setAngle(180)
            if self.scene.myTank.x > 40 :
                self.setSpeed(3)           
        elif keys[pygame.K_d]:
            self.setAngle(0)
            if self.scene.myTank.x < 760:
                self.setSpeed(3)
        elif keys[pygame.K_w]:
            self.setAngle(90)
            if self.scene.myTank.y > 35:
                self.setSpeed(3)
        elif keys[pygame.K_s]:
            self.setAngle(270)
            if self.scene.myTank.y < 565:
                self.setSpeed(3)
        else:
            self.setSpeed(0)
            
        
        if keys[pygame.K_j]:
            if self.scene.myBullet.x < 0 and self.scene.myBullet.y < 0:
                self.scene.myBullet.fire()
                self.scene.sound_attack_begin.play()

    def reset(self):
        self.setPosition(100, 500)
        self.setAngle(90)
        self.setSpeed(0)

#Game界面中我方坦克的炮弹
class My_Bullet(gameEngine.SuperSprite):
    
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("bullet.gif")
        self.imageMaster = pygame.transform.scale(self.imageMaster, (7, 7))
        self.setBoundAction(self.HIDE)
        self.reset()
        self.is_inScreen = False


    def checkEvents(self):
        self.checkBounds()

    def fire(self):
        self.setPosition((self.scene.myTank.x, self.scene.myTank.y))
        self.setSpeed(10)
        self.setAngle(self.scene.myTank.rotation)

    def reset(self):
        self.setPosition((-100, -100))
        self.setSpeed(0)

#Game界面中敌军坦克0 和敌军炮弹0
class Enemy_Tank0(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("tank_2.gif")
        self.setPosition((200, 100))
        self.setAngle(90)
        self.setBoundAction(self.STOP)

        self.timeRandom = 0
        self.angleRandom = 0

    def checkEvents(self):

        #敌军坦克的自主化前进和发射，通过Random来实现
        self.timeRandom -= 1
        if self.timeRandom < 0 :
            self.angleRandom = random.randrange(0, 360)
            self.timeRandom = random.randrange(8,20)
        
        if self.angleRandom < 45:
            self.setAngle(180)
            if self.scene.enemyTank0.x > 40 :
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        elif self.angleRandom < 90:
            self.setAngle(0)
            if self.scene.enemyTank0.x < 760:
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        elif self.angleRandom < 135:
            self.setAngle(90)
            if self.scene.enemyTank0.y > 35:
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        elif self.angleRandom < 180:
            self.setAngle(270)
            if self.scene.enemyTank0.y < 565:
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        else:
            self.setSpeed(0)
            
        
        fireRandom = random.randrange(0,100)
        if fireRandom < 40:
            if self.scene.enemyBullet0.x < 0 and self.scene.enemyBullet0.y < 0:
                self.scene.enemyBullet0.fire()
                self.scene.sound_attack_begin.play()

    def reset(self):
        x_rand = random.randrange(30, 770)
        y_rand = random.randrange(30, 570)
        self.setPosition((x_rand, y_rand))
        self.setAngle(90)
        self.setSpeed(0)

class Enemy_Bullet0(gameEngine.SuperSprite):
    
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("bullet_red.png")
        self.imageMaster = pygame.transform.scale(self.imageMaster, (7, 7))
        self.setBoundAction(self.HIDE)
        self.reset()
        self.is_inScreen = False


    def checkEvents(self):
        self.checkBounds()

    def fire(self):
        self.setPosition((self.scene.enemyTank0.x, self.scene.enemyTank0.y))
        self.setSpeed(10)
        self.setAngle(self.scene.enemyTank0.rotation)

    def reset(self):
        self.setPosition((-100, -100))
        self.setSpeed(0)

#Game界面中敌军坦克1 和敌军炮弹1
class Enemy_Tank1(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("tank_2.gif")
        self.setPosition((300, 100))
        self.setAngle(90)
        self.setBoundAction(self.STOP)

        self.timeRandom = 0
        self.angleRandom = 0

    def checkEvents(self):

        self.timeRandom -= 1
        if self.timeRandom < 0 :
            self.angleRandom = random.randrange(0, 360)
            self.timeRandom = random.randrange(8,20)
        
        if self.angleRandom < 45:
            self.setAngle(180)
            if self.scene.enemyTank1.x > 40 :
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        elif self.angleRandom < 90:
            self.setAngle(0)
            if self.scene.enemyTank1.x < 760:
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        elif self.angleRandom < 135:
            self.setAngle(90)
            if self.scene.enemyTank1.y > 35:
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        elif self.angleRandom < 180:
            self.setAngle(270)
            if self.scene.enemyTank1.y < 565:
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        else:
            self.setSpeed(0)
            
        
        fireRandom = random.randrange(0,100)
        if fireRandom < 40:
            if self.scene.enemyBullet1.x < 0 and self.scene.enemyBullet1.y < 0:
                self.scene.enemyBullet1.fire()
                self.scene.sound_attack_begin.play()

    def reset(self):
        x_rand = random.randrange(30, 770)
        y_rand = random.randrange(30, 570)
        self.setPosition((x_rand, y_rand))
        self.setAngle(90)
        self.setSpeed(0)

class Enemy_Bullet1(gameEngine.SuperSprite):
    
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("bullet_red.png")
        self.imageMaster = pygame.transform.scale(self.imageMaster, (7, 7))
        self.setBoundAction(self.HIDE)
        self.reset()
        self.is_inScreen = False


    def checkEvents(self):
        self.checkBounds()

    def fire(self):
        self.setPosition((self.scene.enemyTank1.x, self.scene.enemyTank1.y))
        self.setSpeed(10)
        self.setAngle(self.scene.enemyTank1.rotation)

    def reset(self):
        self.setPosition((-100, -100))
        self.setSpeed(0)

#Game界面中敌军坦克2 和敌军炮弹2
class Enemy_Tank2(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("tank_2.gif")
        self.setPosition((400, 100))
        self.setAngle(90)
        self.setBoundAction(self.STOP)

        self.timeRandom = 0
        self.angleRandom = 0

    def checkEvents(self):

        self.timeRandom -= 1
        if self.timeRandom < 0 :
            self.angleRandom = random.randrange(0, 360)
            self.timeRandom = random.randrange(8,20)
        
        if self.angleRandom < 45:
            self.setAngle(180)
            if self.scene.enemyTank2.x > 40 :
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        elif self.angleRandom < 90:
            self.setAngle(0)
            if self.scene.enemyTank2.x < 760:
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        elif self.angleRandom < 135:
            self.setAngle(90)
            if self.scene.enemyTank2.y > 35:
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        elif self.angleRandom < 180:
            self.setAngle(270)
            if self.scene.enemyTank2.y < 565:
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        else:
            self.setSpeed(0)
            
        
        fireRandom = random.randrange(0,100)
        if fireRandom < 40:
            if self.scene.enemyBullet2.x < 0 and self.scene.enemyBullet2.y < 0:
                self.scene.enemyBullet2.fire()
                self.scene.sound_attack_begin.play()

    def reset(self):
        x_rand = random.randrange(30, 770)
        y_rand = random.randrange(30, 570)
        self.setPosition((x_rand, y_rand))
        self.setAngle(90)
        self.setSpeed(0)

class Enemy_Bullet2(gameEngine.SuperSprite):
    
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("bullet_red.png")
        self.imageMaster = pygame.transform.scale(self.imageMaster, (7, 7))
        self.setBoundAction(self.HIDE)
        self.reset()
        self.is_inScreen = False


    def checkEvents(self):
        self.checkBounds()

    def fire(self):
        self.setPosition((self.scene.enemyTank2.x, self.scene.enemyTank2.y))
        self.setSpeed(10)
        self.setAngle(self.scene.enemyTank2.rotation)

    def reset(self):
        self.setPosition((-100, -100))
        self.setSpeed(0)


#Game界面中敌军坦克3 和敌军炮弹3    
class Enemy_Tank3(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("tank_2.gif")
        self.setPosition((500, 100))
        self.setAngle(90)
        self.setBoundAction(self.STOP)

        self.timeRandom = 0
        self.angleRandom = 0

    def checkEvents(self):

        self.timeRandom -= 1
        if self.timeRandom < 0 :
            self.angleRandom = random.randrange(0, 360)
            self.timeRandom = random.randrange(8,20)
        
        if self.angleRandom < 45:
            self.setAngle(180)
            if self.scene.enemyTank3.x > 40 :
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        elif self.angleRandom < 90:
            self.setAngle(0)
            if self.scene.enemyTank3.x < 760:
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        elif self.angleRandom < 135:
            self.setAngle(90)
            if self.scene.enemyTank3.y > 35:
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        elif self.angleRandom < 180:
            self.setAngle(270)
            if self.scene.enemyTank3.y < 565:
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        else:
            self.setSpeed(0)
            
        
        fireRandom = random.randrange(0,100)
        if fireRandom < 40:
            if self.scene.enemyBullet3.x < 0 and self.scene.enemyBullet3.y < 0:
                self.scene.enemyBullet3.fire()
                self.scene.sound_attack_begin.play()

    def reset(self):
        x_rand = random.randrange(30, 770)
        y_rand = random.randrange(30, 570)
        self.setPosition((x_rand, y_rand))
        self.setAngle(90)
        self.setSpeed(0)

class Enemy_Bullet3(gameEngine.SuperSprite):
    
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("bullet_red.png")
        self.imageMaster = pygame.transform.scale(self.imageMaster, (7, 7))
        self.setBoundAction(self.HIDE)
        self.reset()
        self.is_inScreen = False


    def checkEvents(self):
        self.checkBounds()

    def fire(self):
        self.setPosition((self.scene.enemyTank3.x, self.scene.enemyTank3.y))
        self.setSpeed(10)
        self.setAngle(self.scene.enemyTank3.rotation)

    def reset(self):
        self.setPosition((-100, -100))
        self.setSpeed(0)


#Game界面中敌军坦克4 和敌军炮弹4   
class Enemy_Tank4(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("tank_2.gif")
        self.setPosition((600, 100))
        self.setAngle(90)
        self.setBoundAction(self.STOP)

        self.timeRandom = 0
        self.angleRandom = 0

    def checkEvents(self):

        self.timeRandom -= 1
        if self.timeRandom < 0 :
            self.angleRandom = random.randrange(0, 360)
            self.timeRandom = random.randrange(8,20)
        
        if self.angleRandom < 45:
            self.setAngle(180)
            if self.scene.enemyTank4.x > 40 :
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        elif self.angleRandom < 90:
            self.setAngle(0)
            if self.scene.enemyTank4.x < 760:
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        elif self.angleRandom < 135:
            self.setAngle(90)
            if self.scene.enemyTank4.y > 35:
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        elif self.angleRandom < 180:
            self.setAngle(270)
            if self.scene.enemyTank4.y < 565:
                self.setSpeed(3)
            else:
                self.setSpeed(0)
        else:
            self.setSpeed(0)
            
        
        fireRandom = random.randrange(0,100)
        if fireRandom < 40:
            if self.scene.enemyBullet4.x < 0 and self.scene.enemyBullet4.y < 0:
                self.scene.enemyBullet4.fire()
                self.scene.sound_attack_begin.play()

    def reset(self):
        x_rand = random.randrange(30, 770)
        y_rand = random.randrange(30, 570)
        self.setPosition((x_rand, y_rand))
        self.setAngle(90)
        self.setSpeed(0)

class Enemy_Bullet4(gameEngine.SuperSprite):
    
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("bullet_red.png")
        self.imageMaster = pygame.transform.scale(self.imageMaster, (7, 7))
        self.setBoundAction(self.HIDE)
        self.reset()
        self.is_inScreen = False


    def checkEvents(self):
        self.checkBounds()

    def fire(self):
        self.setPosition((self.scene.enemyTank4.x, self.scene.enemyTank4.y))
        self.setSpeed(10)
        self.setAngle(self.scene.enemyTank4.rotation)

    def reset(self):
        self.setPosition((-100, -100))
        self.setSpeed(0)


#Game主界面
class Game(gameEngine.Scene):

    #界面初始化
    def __init__(self):
        gameEngine.Scene.__init__(self)
        
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))


        self.myTank = My_Tank(self)
        self.myBullet = My_Bullet(self)

        self.enemyTank0 = Enemy_Tank0(self)
        self.enemyBullet0 = Enemy_Bullet0(self)
        
        self.enemyTank1 = Enemy_Tank1(self)
        self.enemyBullet1 = Enemy_Bullet1(self)
        
        self.enemyTank2 = Enemy_Tank2(self)
        self.enemyBullet2 = Enemy_Bullet2(self)
        
        self.enemyTank3 = Enemy_Tank3(self)
        self.enemyBullet3 = Enemy_Bullet3(self)
        
        self.enemyTank4 = Enemy_Tank4(self)
        self.enemyBullet4 = Enemy_Bullet4(self)
        

        self.buildSideWalls()
        self.score = 0
        self.addLabels()
        

        self.timeCounter = 60
        self.delay = 30
        self.pause = self.delay

        self.sound_attack_begin = pygame.mixer.Sound("attack_begin.wav")
        self.sound_be_attacked = pygame.mixer.Sound("be_attacked.wav")
        self.sound_beginning = pygame.mixer.Sound("beginning.wav")
        self.sound_gameEnd = pygame.mixer.Sound("gameEnd.wav")

        self.bugCorrect = 0
        self.is_gameEnd = False
        self.is_rePlay = False

        self.wallSprite = self.makeSpriteGroup(self.walls)
        

        self.sprites = [self.label_winner,
                        self.label_score,
                        self.label_timeCounter,
                        self.walls,
                        self.myBullet,
                        self.myTank,
                        self.enemyBullet0,
                        self.enemyTank0,
                        self.enemyBullet1,
                        self.enemyTank1,
                        self.enemyBullet2,
                        self.enemyTank2,
                        self.enemyBullet3,
                        self.enemyTank3,
                        self.enemyBullet4,
                        self.enemyTank4
                        ]
        

    #Game界面四周墙壁
    def buildSideWalls(self):
        self.walls = []
        for i in range(0, 840, 40):
            self.newWall = Wall(self)
            self.newWall.setPosition((i, 0))
            self.walls.append(self.newWall)
        for i in range(0, 840, 40):
            self.newWall = Wall(self)
            self.newWall.setPosition((i, 600))
            self.walls.append(self.newWall)
        for i in range(0, 640, 40):
            self.newWall = Wall(self)
            self.newWall.setPosition((0, i))
            self.walls.append(self.newWall)
        for i in range(0, 640, 40):
            self.newWall = Wall(self)
            self.newWall.setPosition((800, i))
            self.walls.append(self.newWall)
    

    #Game界面中的标签
    def addLabels(self):
        self.label_score = gameEngine.MultiLabel()
        self.label_score.bgColor = (0, 0, 0)
        self.label_score.fgColor = (255, 255, 255)
        self.label_score.font = pygame.font.SysFont("None", 30)
        self.label_score.size = (400, 60)
        self.label_score.center = (70, 70)

        self.label_timeCounter = gameEngine.MultiLabel()
        self.label_timeCounter.bgColor = (0, 0, 0)
        self.label_timeCounter.fgColor = (255, 255, 255)
        self.label_timeCounter.font = pygame.font.SysFont("None", 60)
        self.label_timeCounter.size = (400, 60)
        self.label_timeCounter.center = (400, 100)
        
        self.label_winner = gameEngine.MultiLabel()
        self.label_winner.bgColor = (0, 0, 0)
        self.label_winner.fgColor = (255, 255, 255)
        self.label_winner.font = pygame.font.SysFont("None", 60)
        self.label_winner.size = (700, 125)
        self.label_winner.center = (-500, -500)
        self.label_winner.textLines = ["Game Over, Score is:  "+ str(self.score), "Press SPACE to replay !"]

    #Game Over时的事件监听
    def doEvents(self, event):
        if self.is_gameEnd == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.is_rePlay = True
                    self.keepGoing = False
                if event.key == pygame.K_ESCAPE:
                    exit()


    #Game 界面的刷新操作（这里是比较重点的地方）
    def update(self):

        if self.bugCorrect == 1 and self.is_gameEnd == False:

            #我方坦克打击地方坦克0号
            #击中后，播放声音，我方炮弹重置，敌方0号坦克重置
            myTankShootEnemyTank0 = self.myBullet.collidesWith(self.enemyTank0)
            if myTankShootEnemyTank0 == True:
                self.sound_be_attacked.play()
                self.score += 1
                self.enemyTank0.reset()
                self.myBullet.reset()

            #我方坦克打击地方坦克1号
            myTankShootEnemyTank1 = self.myBullet.collidesWith(self.enemyTank1)
            if myTankShootEnemyTank1 == True:
                self.sound_be_attacked.play()
                self.score += 1
                self.enemyTank1.reset()
                self.myBullet.reset()

            #我方坦克打击地方坦克2号
            myTankShootEnemyTank2 = self.myBullet.collidesWith(self.enemyTank2)
            if myTankShootEnemyTank2 == True:
                self.sound_be_attacked.play()
                self.score += 1
                self.enemyTank2.reset()
                self.myBullet.reset()
                
            #我方坦克打击地方坦克3号
            myTankShootEnemyTank3 = self.myBullet.collidesWith(self.enemyTank3)
            if myTankShootEnemyTank3 == True:
                self.sound_be_attacked.play()
                self.score += 1
                self.enemyTank3.reset()
                self.myBullet.reset()

            #我方坦克打击地方坦克4号
            myTankShootEnemyTank4 = self.myBullet.collidesWith(self.enemyTank4)
            if myTankShootEnemyTank4 == True:
                self.sound_be_attacked.play()
                self.score += 1
                self.enemyTank4.reset()
                self.myBullet.reset()


            #敌方坦克击中我方坦克的处理
            #我方坦克被击中后，游戏结束，展示得分
            enemyTankShootMyTank0 = self.enemyBullet0.collidesWith(self.myTank)
            enemyTankShootMyTank1 = self.enemyBullet1.collidesWith(self.myTank)
            enemyTankShootMyTank2 = self.enemyBullet2.collidesWith(self.myTank)
            enemyTankShootMyTank3 = self.enemyBullet3.collidesWith(self.myTank)
            enemyTankShootMyTank4 = self.enemyBullet4.collidesWith(self.myTank)

            if enemyTankShootMyTank0 == True:
                self.myTank.setPosition((-100, -100))
                self.timeCounter = 0
            if enemyTankShootMyTank1 == True:
                self.myTank.setPosition((-100, -100))
                self.timeCounter = 0
            if enemyTankShootMyTank2 == True:
                self.myTank.setPosition((-100, -100))
                self.timeCounter = 0
            if enemyTankShootMyTank3 == True:
                self.myTank.setPosition((-100, -100))
                self.timeCounter = 0
            if enemyTankShootMyTank4 == True:
                self.myTank.setPosition((-100, -100))
                self.timeCounter = 0
                
            self.label_score.textLines = ["Score:" + str(self.score)]
            self.label_timeCounter.textLines = [str(self.timeCounter)]
        
        if self.timeCounter == 0:
            
            if self.is_gameEnd == False:
                self.sound_gameEnd.play()

            self.is_gameEnd = True

            self.label_winner.center = ((400, 350))

        self.pause -= 1
        if self.pause <= 0:
            self.pause = self.delay
            self.timeCounter -= 1

        if self.bugCorrect == 0:
            self.sound_beginning.play()
            self.bugCorrect += 1
            

def main():
    intro = Intro()
    game = Game()
    intro.start()

    if intro.is_gameTime == True:
        intro.stop()
        game.start()

    while game.is_rePlay == True:
        game = Game()
        game.start()
        game.stop()
    

if __name__ == "__main__":
    main()







