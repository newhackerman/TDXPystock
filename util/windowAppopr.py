# -*- coding: UTF-8
import pywinauto
from pywinauto import application
from pywinauto.application import *
from pywinauto import mouse
from pywinauto import keyboard
from pywinauto import findwindows
import win32api
import time

class windowAppopr(object):
    """
    pywin framwork main class
    tool_name : 程序名称，支持带路径
    windows_name : 窗口名字
    """
    SLEEP_TIME = 1
    # m=mouse()
    # k=keyboard()

    def __init__(self):
        """
        初始化方法，初始化一个app
        """
        self.app = application.Application()

    def start(self, tool_name):
        """
        启动应用程序
        """
        self.app.start(tool_name)
        time.sleep(1)

    def connect(self, window_name,class_name):
        """ 这些参数可以通过spy++ 工具定位到
        连接应用程序
        app.connect_(path = r"c:\windows\system32\notepad.exe")
        app.connect_(process = 2341)
        app.connect_(handle = 0x010f0c)
        class_name#
        """
        self.app.connect(title = window_name,class_name=class_name)
        time.sleep(1)

    def connectForHandle(self, window_name, handle):
        """ 这些参数可以通过spy++ 工具定位到
        连接应用程序
        app.connect_(path = r"c:\windows\system32\notepad.exe")
        app.connect_(process = 2341)
        app.connect_(handle = 0x010f0c)
        class_name#
        """
        self.app.connect(title=window_name, handle=handle)
        time.sleep(1)

    def connectForProcess(self, window_name, process):
        """ 这些参数可以通过spy++ 工具定位到
        连接应用程序
        app.connect_(path = r"c:\windows\system32\notepad.exe")
        app.connect_(process = 2341)
        app.connect_(handle = 0x010f0c)
        class_name#
        """
        self.app.connect(title=window_name, process=process)
        time.sleep(1)

    def connectForPath(self, window_name, path):
        """ 这些参数可以通过spy++ 工具定位到
        连接应用程序
        app.connect_(path = r"c:\windows\system32\notepad.exe")
        app.connect_(process = 2341)
        app.connect_(handle = 0x010f0c)
        class_name#
        """
        self.app.connect(title=window_name, path=path)
        time.sleep(1)

    def close(self, window_name):
        """
        关闭应用程序
        """
        self.app[window_name].Close()
        time.sleep(1)

    def max_window(self, window_name):
        """
        最大化窗口
        """
        self.app[window_name].Maximize()
        time.sleep(1)

    def menu_click(self, window_name, menulist):
        """
        菜单点击
        """
        self.app[window_name].MenuSelect(menulist)
        time.sleep(1)

    def input(self, window_name, controller, content):
        """
        输入内容
        """
        self.app[window_name][controller].TypeKeys(content)
        time.sleep(1)

    def click(self, window_name, controller):
        """
        鼠标左键点击
        example:
        下面两个功能相同,下面支持正则表达式
        app[u'关于“记事本”'][u'确定'].Click()
        app.window_(title_re = u'关于“记事本”').window_(title_re = u'确定').Click()
        """
        self.app[window_name][controller].Click()
        time.sleep(1)


    def double_click(self, window_name, controller, x = 0,y = 0):
        """
        鼠标左键点击(双击)
        """
        self.app[window_name][controller].DoubleClick(button = "left", pressed = "",  coords = (x, y))
        time.sleep(1)

    def right_click(self, window_name, controller, order):
        """
        鼠标右键点击，下移进行菜单选择
        window_name : 窗口名
        controller：区域名
        order ： 数字，第几个命令
        """
        self.app[window_name][controller].RightClick()
        for down in range(order):
            mouse.right_click(coords=(0, 0))
            time.sleep(0.5)
        mouse.right_click()
        time.sleep(1)

    def findwindows(self,**kwargs):
        findwindows.find_windows(**kwargs)

    def topwindow(self,app):
        app.window()
    #获取当前鼠标位置
    def GetCursorPos(self):
        while True:
            print(win32api.GetCursorPos())
            time.sleep(3)

if __name__ == '__main__':
    # app=windowAppopr()
    # tool_name='calc.exe'
    # window_name='计算器'
    # class_name='Windows.UI.Core.CoreWindow'
    # controller='ApplicationFrameInputSinkWindow'
    # content=[0,1,2,3,4,5,6,7,8,9,'+','-','*','/','=']
    # app.start(tool_name)
    # app.connect(window_name,class_name)
    # # app.click(window_name,controller)
    # for i in content:
    #     app.input(window_name,'',i)
    #     time.sleep(2)
    # app.close(window_name)

    app = windowAppopr()
    tool_name = r'C:\十档行情\tdxw.exe'
    window_title='通达信金融终端通赢版V7.47'
    window_class='#32770 (Dialog)'
    processid='00003FA0'
    window_name = '通达信金融终端通赢版V7.47'
    class_name = '#32770 (Dialog)'
    window_title_class = 'AfxWnd42'
    app.start(tool_name)
    app.connectForPath(window_name,tool_name)
    mouse.move([985,420])
    mouse.click('left',[985,420])  #左键在什么位置点击
    time.sleep(10) #休息8秒，等等数据初始化加载
    # app.GetCursorPos()
    #点击A股，导出所有A股早盘数据
    mouse.click('left', [970, 990])
    ###点击选项数据导出，导出数据
    mouse.click('left',[1608, 11])
    mouse.click('left', [1655, 404])
    time.sleep(1)
    mouse.click('left', [827, 397])
    mouse.click('left', [1055, 547])
    time.sleep(1)
    mouse.click('left', [1110, 653])
    app.GetCursorPos()
    time.sleep(60)
    #点击取消，完成导出
    mouse.click('left', [1035, 583])
    time.sleep(1)
    ###########导出版块早盘数据
    # 点击版本块指数，导出所有版块数据
    mouse.click('left', [710, 995])
    mouse.click('left', [42, 67])
    ###点击选项数据导出，导出数据
    mouse.click('left', [1608, 11])
    mouse.click('left', [1655, 404])
    time.sleep(1)
    mouse.click('left', [827, 397])
    mouse.click('left', [1055, 547])
    time.sleep(1)
    mouse.click('left', [1110, 653])
    app.GetCursorPos()
    time.sleep(60)
    # 点击取消，完成导出
    mouse.click('left', [1016, 580])
    # mouse.click('left', [67, 60])
    # mouse.click('left', [108, 398])
    # mouse.click('left', [775, 275])
    # mouse.click('left', [252, 538])
    # mouse.click('left', [336, 174])
    # mouse.click('left', [775, 595])
    # time.sleep(1)
    # mouse.click('left', [773, 589])
    # mouse.click('left', [1021, 528])
    # mouse.click('left', [1892, 20])
    # ###完成导出

    # app1=application.Application()
    # app1.start(tool_name)
    #
    # app1.connect(path=tool_name)
    # list=pywinauto.findwindows(backend='win32')
    # print(list)
    #
    # butt_handle='01F30EDA'
    # # app.click(window_name,'AfxWnd421')
    # app.click(window_title,['CheckBox2'])
