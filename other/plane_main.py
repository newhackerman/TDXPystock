import pygame
from other.plane_sprites import *

class PlaneGame(object):
    def __init__(self):
        #super().__init__()
        #创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.szie)
        #创建游戏时钟
        self.clock = pygame.time.Clock()
        #调用私有方法完成精灵与精灵组的创建
        self.__create_sprites()
        print('游戏初始化')

    def start_game(self):
        print('游戏开始。。。')
        while True:
            #设置刷新帧率
            self.clock.tick(60)
            #事件监听
            self.__event_hander()
            # 碰撞检测
            self.__check_ollide()
            ##更新绘置精灵组
            self.__update_sprites()

            pass

    def __event_hander(self):
        for event in pygame.event.get():




            if event.type==pygame.QUIT:  #退出
                pygame.quit()   #卸载
                exit()          #退出
        pass

    def __check_ollide(self):
        pass

    def __update_sprites(self):
        pass

    @staticmethod
    def __over_game():
        pygame.quit()
        exit()






    def __create_sprites(self):
        pass

    # def game_over(self):
    #     pygame.quit()
    #     exit()

if __name__ == '__main__':
    game=PlaneGame()
    game.__init__()
    game.start_game()
