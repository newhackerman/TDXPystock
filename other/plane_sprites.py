import pygame

#定义屏幕大小
SCREEN_RECT=pygame.Rect(0,0,480,700)

class Gamesprite(pygame.sprite.Sprite) :

    def __init__(self,image_name,speed=1):
        super().__init__()
        self.image=pygame.image.load(image_name)
        self.rect=self.image.get_rect()
        self.speed=speed

    def update(self) :
        #在屏幕的垂直方向上移动
        self.rect.y+=self.speed
        pass

