import pygame
from other.plane_sprites import *
pygame.init()
screen=pygame.display.set_mode((480,700)) #设置窗口大小
bg=pygame.image.load('./images/background.png')
screen.blit(bg,(1,1))
hreo=pygame.image.load('./images/me1.png') #加载图片文件
screen.blit(hreo,(200,600)) #设置图片加载的位置
pygame.display.update() #更新画面
clock=pygame.time.Clock() #时钟
hreo_rect=pygame.Rect(200,600,78,95)  #确定坐标  78，95 为图片的长宽
enemy=Gamesprite('./images/enemy1.png')  #创建敌机
enemy2=Gamesprite('./images/enemy1.png',2)
enemy_group=pygame.sprite.Group(enemy,enemy2)
i=0
while True:
    clock.tick(60)
    i+=1
    if i<=600:
        eventlist=pygame.event.get() #监听事件
        for event in eventlist:
            if event.type==pygame.QUIT:  #退出
                pygame.quit()   #卸载
                exit()          #退出


        if len(eventlist)>0:
            print(eventlist)
        hreo_rect.y-=1
        screen.blit(bg, (1, 1))            #重新绘置一遍前景
        screen.blit(hreo,hreo_rect)        #再绘置一下前景

        enemy.update()  #
        enemy_group.draw(screen)
        enemy2.update()  #

        pygame.display.update()
    else:
        hreo_rect=pygame.Rect(200,600,78,95)


pygame.quit()

