import pygame
from random import *


class SmallEnemy(pygame.sprite.Sprite):
    energy=1  #血，被普通子弹击中多少下死掉
    score=20 #打死后的分数
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("images/enemy1.png").convert_alpha()
        self.destroy_images=[]
        self.destroy_images.extend([\
            pygame.image.load("images/enemy1_down1.png").convert_alpha(),\
            pygame.image.load("images/enemy1_down2.png").convert_alpha(),\
            pygame.image.load("images/enemy1_down3.png").convert_alpha(),\
            pygame.image.load("images/enemy1_down4.png").convert_alpha()\
            ])
        self.rect=self.image.get_rect()
        self.width,self.height=bg_size[0],bg_size[1]
        self.speed=randint(3,5)
        self.active = True
        self.rect.left,self.rect.top=\
        randint(0,self.width-self.rect.width),randint(-5*self.height,0)
        self.mask = pygame.mask.from_surface(self.image)
        self.energy=SmallEnemy.energy

    def move(self):
        if self.rect.top<self.height:
            self.rect.top+=self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), randint(-5 * self.height, 0)
        self.energy=SmallEnemy.energy

class midEnemy(pygame.sprite.Sprite):
    energy = 8 #血，被普通子弹击中多少下死掉
    score=50  #被打死后的分数
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("images/enemy2.png").convert_alpha()
        self.image_hit = pygame.image.load("images/enemy2_hit.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([ \
            pygame.image.load("images/enemy2_down1.png").convert_alpha(), \
            pygame.image.load("images/enemy2_down2.png").convert_alpha(), \
            pygame.image.load("images/enemy2_down3.png").convert_alpha(), \
            pygame.image.load("images/enemy2_down4.png").convert_alpha() \
            ])
        self.rect=self.image.get_rect()
        self.width,self.height=bg_size[0],bg_size[1]
        self.speed=1    #移动速度
        self.active = True  #是否死亡

        self.rect.left,self.rect.top=\
        randint(-10,self.width-self.rect.width),randint(-self.height,0)

        self.mask = pygame.mask.from_surface(self.image)  #是否相撞
        self.energy=midEnemy.energy  #生命值
        self.hit=False  #是否被 击中
        self.score=midEnemy.score
    def move(self):
        if self.rect.top<self.height:
            self.rect.top+=self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = \
            randint(-10, self.width - self.rect.width), randint(- self.height, 0)
        self.energy=midEnemy.energy

class bigEnemy(pygame.sprite.Sprite):
    energy=15    #血，被普通子弹击中多少下死掉
    score=150 #打死后分数
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1=pygame.image.load("images/enemy3_n1.png").convert_alpha()
        self.image2=pygame.image.load("images/enemy3_n2.png").convert_alpha()
        self.image_hit=pygame.image.load("images/enemy3_hit.png").convert_alpha()

        self.destroy_images = []
        self.destroy_images.extend([ \
            pygame.image.load("images/enemy3_down1.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down2.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down3.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down4.png").convert_alpha(),
            pygame.image.load("images/enemy3_down5.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down6.png").convert_alpha() \
            ])
        self.rect=self.image1.get_rect()
        self.width,self.height=bg_size[0],bg_size[1]
        self.speed=1
        self.active=True
        self.rect.left,self.rect.top=\
        randint(-15,self.width-self.rect.width),randint(-5*self.height,0)
        self.mask = pygame.mask.from_surface(self.image1)
        self.energy=bigEnemy.energy
        self.hit = False  # 是否被 击中
        self.score=bigEnemy.score
    def move(self):
        if self.rect.top<self.height:
            self.rect.top+=self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = \
            randint(-15, self.width - self.rect.width), randint(-5* self.height, 0)
        self.energy=bigEnemy.energy