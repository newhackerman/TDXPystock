import pygame
from pygame.locals import *
import sys
import traceback
import myplance
import enemy
import bullet
import supply
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
getbomb_supply_sound=pygame.mixer.Sound("sound/get_bomb.wav")
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

def add_speed(target,inc):
    for each in target:
        each.speed+=inc

#游戏重置
def reset(target):
    for each in target:

        each.reset

#生成我方飞与敌机，子弹等
def createmainmuple():
   pass

def main():
    pygame.init()
    pygame.mixer.music.play(-1)

    # 生成我方飞机
    me = myplance.MyPlance(bg_size)
    # 生成敌机组
    enemys = pygame.sprite.Group()
    # 生成小型敌机
    small_enemys = pygame.sprite.Group()
    add_small_enemys(small_enemys, enemys, randint(5, 8))
    # 生成中型敌机
    mid_enemys = pygame.sprite.Group()
    add_mid_enemys(mid_enemys, enemys, randint(2, 6))
    # 生成大型敌机
    big_enemys = pygame.sprite.Group()
    add_big_enemys(big_enemys, enemys, randint(1, 3))

    # 生成普通子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))
    #生成二级子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    for j in range(BULLET2_NUM//2):
        bullet2.append(bullet.Bullet2((me.rect.centerx-33,me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx+30,me.rect.centery)))
    #print("子弹总数",j*2)
    #定义时钟
    clock = pygame.time.Clock()
    #定义是否重新开始
    replay=False


    score_font=pygame.font.Font("font/font.ttf",36) #加载字体

    #标记游戏是否暂停
    paused=True
    paused_nor_image=pygame.image.load("images/pause_nor.png").convert_alpha()
    paused_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
    paused_rect=paused_nor_image.get_rect()
    paused_rect.left,paused_rect.top=width-paused_rect.width-10,10
    paused_image=paused_nor_image

    #设置全屏炸弹
    bomb_image=pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect=bomb_image.get_rect()
    bomb_num=3 #初始全屏炸弹个数
    bomb_font=pygame.font.Font("font/font.ttf",36)
    life_font = pygame.font.Font("font/font.ttf", 36)
    #中弹图片索引
    e1_destroy_index=0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0
    #用于切换图片
    switch_image=True
    #游戏结束画面
    gameover_font=pygame.font.Font("font/font.TTF",36)
    again_iamge=pygame.image.load("images/again.png").convert_alpha()
    again_rect=again_iamge.get_rect()
    gameover_image=pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect=gameover_image.get_rect()


    #用于延时
    delay=100
    #每30秒发放一个
    supplygettime=30
    bullet_supply=supply.Bullet_Suply(bg_size)
    bomb_supply=supply.Bomb_Suply(bg_size)
    SUPPLY_TIME=USEREVENT
    pygame.time.set_timer(SUPPLY_TIME,supplygettime*1000)

    #超级子弹定时器
    DOUBLEBUF_TIME=USEREVENT+1
    #累计可获得全屏炸弹个数
    MAX_BOMB_NUM=10
    # 二级子弹状态
    is_double_bullet = False
    #获得补给使用有效时间
    supperbombusetime=18
    #是否写记录到文件
    recordread=False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==MOUSEBUTTONDOWN:
                #暂停游戏
                if event.button==1 and paused_rect.collidepoint(event.pos):
                    paused=not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME,0)
                        pygame.time.set_timer(DOUBLEBUF_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()#暂停所有声音
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, supplygettime*1000)
                        pygame.time.set_timer(SUPPLY_TIME, DOUBLEBUF_TIME * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            elif event.type==MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image=resume_pressed_image
                    else:
                        paused_image=paused_pressed_image

            #当按下B键，释放超级炸雷
            elif event.type==KEYDOWN:
                if event.key==K_b:
                    if bomb_num:
                        bomb_num-=1
                        bomb_sound.play()
                        for each in enemys:
                            if each.rect.bottom>0:
                                each.active=False
                        # 当按下B键，释放超级炸雷
                #当按下V键继续
                if event.key == K_v:
                    if paused:
                        paused=not paused
            #超级补给事件
            elif event.type==SUPPLY_TIME:
                supply_sound.play()
                if choice([True,False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            #超级炸弹事件
            elif event.type==DOUBLEBUF_TIME:
                is_double_bullet=False
                pygame.time.set_timer(DOUBLEBUF_TIME,0)




        # 根据用户的得分增加难度
        if me.level == 1 and me.score >= me.score_level1:
            me.level = 2
            upgrade_sound.play()
            # 增加3加小型机2架中型敌机，1架大型敌机
            add_small_enemys(small_enemys, enemys, 3)
            add_mid_enemys(mid_enemys, enemys, 2)
            add_big_enemys(big_enemys, enemys, 1)
            # 增加敌机1的速度
            #add_speed(small_enemys, 1)
            #增加子弹的速度
            # add_speed(bullet1,5)
        elif me.level == 2 and me.score >= me.score_level2:
            me.level = 3
            upgrade_sound.play()
            # 增加5加小型机3架中型敌机，2架大型敌机
            add_small_enemys(small_enemys, enemys, 5)
            add_mid_enemys(mid_enemys, enemys, 3)
            add_big_enemys(big_enemys, enemys, 2)
            # 增加敌机1的速度
            # add_speed(small_enemys, 1)
            # add_speed(mid_enemys, 1)
            #增加子弹的速度
            # add_speed(bullet1,10)
            #增加子弹
            bullets = bullet2
            # bullet2.active=True
            bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
            bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
            #print("bullet2_index+1:", bullet2_index + 1)
            bullet2_index = (bullet2_index + 2) % BULLET2_NUM
        elif me.level == 3 and me.score >= me.score_level3:
            me.level = 4
            upgrade_sound.play()
            # 增加5加小型机3架中型敌机，2架大型敌机
            add_small_enemys(small_enemys, enemys, 5)
            add_mid_enemys(mid_enemys, enemys, 3)
            add_big_enemys(big_enemys, enemys, 2)
            # 增加敌机1的速度
            # add_speed(small_enemys, 1)
            # add_speed(mid_enemys, 1)
            # add_speed(big_enemys, 1)
            #增加子弹的速度
            # add_speed(bullet1,10)
            # add_speed(bullet2, 10)

        elif me.level == 4 and me.score >= me.score_level4:
            me.level = 5
            upgrade_sound.play()
            # 增加5加小型机3架中型敌机，2架大型敌机
            add_small_enemys(small_enemys, enemys, 5)
            add_mid_enemys(mid_enemys, enemys, 3)
            add_big_enemys(big_enemys, enemys, 2)
            # 增加敌机1的速度
            # 增加敌机1的速度
            # add_speed(small_enemys, 2)
            # add_speed(mid_enemys, 2)
            # add_speed(big_enemys, 2)
            # #增加子弹的速度
            # add_speed(bullet1,10)
            # add_speed(bullet2, 10)

        #绘制背景(放在主流程外，轻微防止作弊)
        screen.blit(background,(0,0))

        #开始主流程
        if me.count >0 and paused:
            # 检测用户的键盘操作
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveleft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()
            #如果按空格键则暂停游戏
            if key_pressed[K_SPACE]:
                paused = not paused

            #绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image,bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply,me):
                    getbomb_supply_sound.play()
                    if bomb_num<MAX_BOMB_NUM:
                        bomb_num+=1
                    bomb_supply.active=False
            #绘制超级子弹补给并检测是否获得
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image,bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply,me):
                    get_bullet_sound.play()
                    is_double_bullet=True   #设置双倍子弹
                    #pygame.time.set_timer(DOUBLEBUF_TIME,supperbombusetime*1000)
                    bullet_supply.active=False
            # 发射超级子弹
            if not(delay%10):
                bullet_sound.play()
                if is_double_bullet:  #获得双倍子弹的情况下，发射二级字弹
                    bullets = bullet2
                    #bullet2.active=True
                    bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
                    print("bullet2_index+1:" ,bullet2_index + 1)
                    bullet2_index = (bullet2_index+2) % BULLET2_NUM
                    # try:
                    #     # if bullet2_index>=BULLET2_NUM:
                    #     #     bullet2_index=0
                    #     bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                    #     bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
                    #     bullet2_index = (bullet2_index + 1) % BULLET2_NUM
                    #
                    # except IndexError as IndexE:
                    #     print(IndexE)
                    #     print("bullet2_index is :",bullet2_index+1)
                else:
                    #print("我的当前位置", me.rect.midtop)
                    bullets=bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index=(bullet1_index+1)%BULLET1_NUM

            #检测子弹是否击中敌机
            for b in bullets:
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
                # 在屏幕左上角显示当前分数：
                score_text = score_font.render("Score :%s" % str(me.score), True, GREEN)
                screen.blit(score_text, (0, 0))
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
                #毁灭
                me_down_sound.play()
                if not(delay%3):
                    screen.blit(me.destroy_images[me_destroy_index],each.rect)
                    me_destroy_index=(me_destroy_index+1)%4
                    if me_destroy_index==0:
                        me.reset()
                        me.count-=1
        # 如果生命值为0时：
        elif me.count==0:
            #停止背景音效
            pygame.mixer.music.stop()
            #停止全部音效
            pygame.mixer.stop()
            #停止发放补给
            pygame.time.set_timer(SUPPLY_TIME,0)
            pygame.time.set_timer(DOUBLEBUF_TIME, 0)
            #如果当前分数大于历史最高分，则保存记录
            if not recordread:
                recordread=True
                if me.score > me.history_score:
                    with open("score.txt",'w') as fr:
                        fr.write(me.score)


            #print("Game Over!")
            #绘制结束画面


            record_score_text=score_font.render("max  %d" %me.history_score,True,WHITE)
            #print(me.history_score)
            screen.blit(record_score_text,(60,60))

            gameover_text1=gameover_font.render("your Score  %d" %me.score,True,WHITE)
            gameover_text1_rect=gameover_text1.get_rect()
            gameover_text1_rect.left,gameover_text1_rect.top=(width-gameover_text1_rect.width)//2,height/2
            screen.blit(gameover_text1,gameover_text1_rect)
            #print("step1")
            # gameover_text2 = gameover_font.render(str(me.score), True, WHITE)
            # gameover_text2_rect = gameover_text2.get_rect()
            # gameover_text2_rect.left, gameover_text2_rect.top = \
            #     (width - gameover_text1_rect.width // 2), gameover_text1_rect.bottom+10
            # screen.blit(gameover_text2, gameover_text2_rect)
            #print("step2")
            again_rect.left, again_rect.top = \
                (width - again_rect.width) // 2, gameover_text1_rect.bottom + 50
            screen.blit(again_iamge, again_rect)

            gameover_rect.left, gameover_rect.top = \
                (width - again_rect.width) // 2, again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)
            #print("step3")
            pygame.display.update()
            #检测用户鼠标操作
            #如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                #print("step4")
                #获取鼠标坐标
                pos=pygame.mouse.get_pos()
                #如果用户点击“重新开始”
                if again_rect.left<pos[0]<again_rect.right and again_rect.top<pos[1]<again_rect.bottom:
                    #调用main()函数 重新开始
                    #print("step5")
                    main()
                #如果 用户点击 “结束游戏”
                elif gameover_rect.left<pos[0]<gameover_rect.right and gameover_rect.top<pos[1]<gameover_rect.bottom:
                    #print("step6")
                    pygame.quit()
                    sys.exit()
        #在左下角绘制全屏炸弹
        bomb_text=bomb_font.render("B %d" %bomb_num,True,WHITE)
        text_rect=bomb_text.get_rect()
        screen.blit(bomb_image,(10,height-10-bomb_rect.height))
        screen.blit(bomb_text, (10+bomb_rect.width,height-5-text_rect.height))

        #在右下角绘制剩余生命数
        if me.count>0:
            life_text=life_font.render("%d" %me.count,True,WHITE)
            life_text_rect=life_text.get_rect()
            screen.blit(me.life_image, (width - 10 -me.life_rect.width-life_text_rect.width, height - 3 - me.life_rect.height))
            screen.blit(life_text,
                        (width - life_text_rect.width, height - 3 - me.life_rect.height))

        #绘制暂停按钮
        screen.blit(paused_image,paused_rect)
        #切换图片
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
