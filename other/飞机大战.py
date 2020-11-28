import pygame
pygame.init()
screen=pygame.display.set_mode((480,700)) #设置窗口大小
bg=pygame.image.load('E:\\手机相关\\华为手机\\壁纸\\magazine-unlock-01-2.3.1009-_7AD45EE0D67ED07E16EB17D8EF5FE114.jpg')
screen.blit(bg,(1,1))
hreo=pygame.image.load('hreo.png') #加载图片文件
screen.blit(hreo,(200,600)) #设置图片加载的位置
pygame.display.update() #更新画面
clock=pygame.time.Clock() #时钟
hreo_rect=pygame.Rect(200,600,78,95)  #确定坐标  78，95 为图片的长宽
i=0
while True:
    clock.tick(60)
    i+=1
    if i<=600:
        event1=pygame.event.get() #监听事件
        print(event1)
        hreo_rect.y-=1
        screen.blit(bg, (1, 1))            #重新绘置一遍前景
        screen.blit(hreo,hreo_rect)        #再绘置一下前景

        pygame.display.update()
    else:
        pass

pygame.quit()

