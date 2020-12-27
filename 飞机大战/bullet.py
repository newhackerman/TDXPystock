import pygame
import myplance

class Bullet1(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("images/bullet1.png").convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=position
        self.speed=12
        self.active=True
        self.mask=pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top-=self.speed

        if self.rect.top<0:
            self.active=False

    def reset(self,position):
        self.rect.left,self.rect.top=position
        self.active=True

#二级子弹
class Bullet2(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("images/bullet2.png").convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=position
        self.speed=25
        self.active=True
        self.mask=pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top-=self.speed

        if self.rect.top<0:
            self.active=False

    def reset(self,position):
        self.rect.left,self.rect.top=position
        self.active=True
#超级出子弹
class Bulletsupper(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("images/bullet_supply.png").convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=position
        self.speed=50
        self.active=True
        self.mask=pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top-=self.speed

        if self.rect.top<0:
            self.active=False

    def reset(self,position):
        self.rect.left,self.rect.top=position
        self.active=True
