import pygame
from pygame.locals import *
import sys
import traceback
import myplance
import enemy
import bullet
from random import *

pygame.init()
pygame.mixer.init()


bg_size=width,height=400,700
screen=pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战")

background=pygame.image.load("images/background.png").convert()
#定义血槽颜色
BLACK=(0,0,0)
GREEN=(0,255,0)
RED=(255,0,0)
WHITE=(255,255,255)
#载入声音
volume=0.2
vol1=0.5
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(volume)
bullet_sound=pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(volume)
bomb_sound=pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(volume)
supply_sound=pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(volume)
get_bullet_sound=pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(volume)
upgrade_sound=pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(volume)

enemy3_fly_sound=pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(volume)
enemy3_down_sound=pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)

enemy2_down_sound=pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(volume)

enemy1_down_sound=pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(volume)

me_down_sound=pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(volume)

def  add_small_enemys(group1,group2,num):
    for i in range(num):
        e1=enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def  add_mid_enemys(group1,group2,num):
    for i in range(num):
        e2=enemy.midEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def  add_big_enemys(group1,group2,num):
    for i in range(num):
        e3=enemy.bigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def main():
    pygame.init()
    pygame.mixer.music.play(-1)

    #生成我方飞机
    me=myplance.MyPlance(bg_size)

    #生成敌机组
    enemys=pygame.sprite.Group()
    #生成小型敌机
    small_enemys=pygame.sprite.Group()
    add_small_enemys(small_enemys,enemys,randint(5,10))
    #生成中型敌机
    mid_enemys = pygame.sprite.Group()
    add_mid_enemys(mid_enemys,enemys, randint(2,6))
    #生成大型敌机
    big_enemys = pygame.sprite.Group()
    add_big_enemys(big_enemys,enemys, randint(1,3))

    #生成普通子弹
    bullet1=[]
    bullet1_index=0
    BULLET1_NUM=4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))


    clock = pygame.time.Clock()
    #用于统计得分
    score=0
    score_font=pygame.font.Font("font/font.ttf",24) #加载字体
    #中弹图片索引
    e1_destroy_index=0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0
    #用于切换图片
    switch_image=True
    #用于延时
    delay=100

    running = True
    while running:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        #检测用户的键盘操作
        key_pressed=pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            me.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            me.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            me.moveleft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            me.moveRight()


        screen.blit(background,(0,0))

        if not(delay%10):
            #print("我的当前位置", me.rect.midtop)
            bullet1[bullet1_index].reset(me.rect.midtop)

            bullet1_index=(bullet1_index+1)%BULLET1_NUM

        #检测子弹是否击中敌机
        for b in bullet1:
            if b.active:
                b.move()
                screen.blit(b.image,b.rect)
                enemy_hit=pygame.sprite.spritecollide(b,enemys,False,pygame.sprite.collide_mask)
                if enemy_hit:
                    b.active=False

                    for e in enemy_hit:
                        if e in mid_enemys or e in big_enemys or e in small_enemys:
                            e.hit=True
                            e. energy-=1
                            if e.energy==0:
                                me.score+=e.score   #敌机死亡后，统计分数
                                e.active=False
                        else:
                            e.active=False
                # 显示分数
                score_text = score_font.render("Score :%s" % str(me.score), True, GREEN)
                screen.blit(score_text, (0, 0))
                #当分数达到500分加2级子弹
                if me.score>=500:
                    pass
                # 当分数达到10500分加超级子弹
                if me.score >= 1500:
                    pass
        #在屏幕左上角显示当前分数：
        # 显示分数
        # score_text = score_font.render("Score :%s" % str(me.score), True, GREEN)
        # screen.blit(score_text, (0, 0))
        #delay-=1
        #绘制大型机
        for each in big_enemys:
            if each.active:
                each.move()
                if each.hit:
                    #绘制被打到的特效
                    screen.blit(each.image_hit,each.rect)
                    each.hit=False
                else:

                    if switch_image:
                        screen.blit(each.image1,each.rect)
                    else:
                        screen.blit(each.image2,each.rect)

                #绘制血量
                pygame.draw.line(screen,BLACK,(each.rect.left,each.rect.top-5),\
                    (each.rect.right,each.rect.top-5),3)

                #当生命值 大于30%时显示绿色 ，否则显示红色
                energy_remain=each.energy/enemy.bigEnemy.energy
                if energy_remain>0.3:
                    energy_color=GREEN
                else:
                    energy_color=RED
                pygame.draw.line(screen,energy_color,(each.rect.left,each.rect.top-5),\
                                 (each.rect.left+each.rect.width*energy_remain,\
                                  each.rect.top-5),2)
                #大型敌机出现在画面中，播放音效
                if each.rect.bottom==-50:
                    enemy3_fly_sound.play(-1)
            else:
                if not(delay%3):
                    if e3_destroy_index==0:
                        enemy3_down_sound.play()
                    screen.blit(each.destroy_images[e3_destroy_index],each.rect)
                    e3_destroy_index=(e3_destroy_index+1)%6
                    if e3_destroy_index==0:
                        enemy3_down_sound.stop()
                        each.reset()
        #绘制中型敌机
        for each in mid_enemys:
            if each.active:
                each.move()
                if each.hit:
                    # 绘制被打到的特效
                    screen.blit(each.image_hit, each.rect)
                    each.hit = False
                else:
                    screen.blit(each.image,each.rect)
                #绘制血量
                pygame.draw.line(screen,BLACK,(each.rect.left,each.rect.top-5),\
                    (each.rect.right,each.rect.top-5),2)

                #当生命值 大于20%时显示绿色 ，否则显示红色
                energy_remain=each.energy/enemy.midEnemy.energy
                if energy_remain>0.2:
                    energy_color=GREEN
                else:
                    energy_color=RED
                pygame.draw.line(screen,energy_color,(each.rect.left,each.rect.top-5),\
                                 (each.rect.left+each.rect.width*energy_remain,\
                                  each.rect.top-5),2)
            else:

                if not (delay % 3):
                    if e2_destroy_index == 0:
                        enemy2_down_sound.play()
                    screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                    e2_destroy_index = (e2_destroy_index + 1) % 4
                    if e2_destroy_index == 0:
                        each.reset()
        # 绘制小型敌机
        for each in small_enemys:
            if each.active:
                each.move()
                screen.blit(each.image, each.rect)
            else:
                if e1_destroy_index == 0:
                    enemy1_down_sound.play()
                if not (delay % 3):
                    screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                    e1_destroy_index = (e1_destroy_index + 1) % 4
                    if e1_destroy_index == 0:
                        each.reset()
        #检测飞机是否被撞
        enemys_down=pygame.sprite.spritecollide(me,enemys,False,pygame.sprite.collide_mask)
        if enemys_down:
            me.active=False
            for e in enemys_down:
                e.active=False

        #绘制我方飞机
        #switch_image=not switch_image
        if me.active:
            if switch_image:
                screen.blit(me.image1,me.rect)
            else:
                screen.blit(me.image2,me.rect)
        else:
            me_down_sound.play()
            if not(delay%3):
                screen.blit(me.destroy_images[me_destroy_index],each.rect)
                me_destroy_index=(me_destroy_index+1)%4
                if me_destroy_index==0:
                    me.reset()


        if not (delay%5):
            switch_image=not switch_image

        #用于延迟
        delay-=-1
        if not delay:
            delay=100
        pygame.init()

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    try:
        main()
    except SystemExit as SE:
        print(SE)
    except:
        traceback.print_exc()
        pygame.QUIT
        input()
