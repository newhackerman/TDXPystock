import pygame
#读取历史记录
def gethistoryscore():
    #history_score=0
    with open('score.txt', 'r') as fr:
        history_score = int(fr.read())
    return history_score

class MyPlance(pygame.sprite.Sprite):
    count=6  #默认6条命
    score=0  #用来统计杀死敌机的分数
    # 难度等级
    level = 1
    # 分数等级
    score_level1 = 500
    score_level2 = 1500
    score_level3 = 5000
    score_level4 = 20000

    def  __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1=pygame.image.load("images/me1.png").convert_alpha()
        self.image2= pygame.image.load("images/me2.png").convert_alpha()
        #将我方图片都加载进来
        self.destroy_images=[]
        self.destroy_images.extend([\
            pygame.image.load("images/me_destroy_1.png").convert_alpha(),\
            pygame.image.load("images/me_destroy_2.png").convert_alpha(),\
            pygame.image.load("images/me_destroy_3.png").convert_alpha(),\
            pygame.image.load("images/me_destroy_4.png").convert_alpha()\
            ])
        self.life_image=pygame.image.load("images/life.png").convert_alpha()
        self.life_rect=self.life_image.get_rect()

        self.rect=self.image1.get_rect()

        self.width,self.height=bg_size[0],bg_size[1]
        self.rect.left,self.rect.top=(self.width-self.rect.width)//2,\
            self.height-self.rect.height-10
        self.speed=6
        self.active=True
        self.mask=pygame.mask.from_surface(self.image1)
        self.score=MyPlance.score
        self.history_score=gethistoryscore()
        self.inviciable=False#无敌状态
    def moveUp(self):
        if self.rect.top>0:
            self.rect.top-=self.speed
        else:
            self.rect.top=0

    def moveDown(self):
        if self.rect.bottom<self.height-10:
            self.rect.top+=self.speed
        else:
            self.rect.bottom=self.height-10

    def moveleft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right< self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width
    def reset(self):
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, \
                                        self.height - self.rect.height - 10
        self.speed = 6
        self.active = True
        self.mask = pygame.mask.from_surface(self.image1)
        #self.score = MyPlance.score
        self.active = True
        self.inviciable=True
        #self.count-=1;
        # if self.count<=0:
        #     #提示是否重新开始
        #     #然后重置游戏
        #
        #     self.count=6
        #     self.score=0
        #     self.level=1
        #

            #pygame.display.flip()
            #pygame.quit()
