###导出通达信数据到EXCEL
import win32api
from pywinauto import application
from pywinauto.application import *
from pywinauto import mouse

def TDX_OpenDataOutput():
    app=application.Application()
    tool_name = r'C:\十档行情\tdxw.exe'
    window_name = '通达信金融终端通赢版V7.47'
    app.start(tool_name)
    time.sleep(3)
    app.connect(path=tool_name)
    time.sleep(2)
    #登录
    mouse.move([985,420])
    mouse.click('left',[990,422])  #左键在什么位置点击
    time.sleep(15) #休息8秒，等等数据初始化加载
    # app.GetCursorPos()
    #点击A股，导出所有A股早盘数据
    mouse.click('left', [970, 990])
    ###点击选项数据导出，导出数据
    mouse.click('left',[1608, 11])
    time.sleep(1)
    mouse.click('left', [1655, 404])
    time.sleep(1)
    mouse.click('left', [827, 397])
    time.sleep(1)
    mouse.click('left', [1055, 547])
    time.sleep(1)
    mouse.click('left', [1110, 653])

    time.sleep(45)
    #点击取消，完成导出
    mouse.click('left', [1035, 583])
    time.sleep(1)
    ###########导出版块早盘数据
    # 点击版本块指数，导出所有版块数据
    mouse.click('left', [710, 995])
    time.sleep(1)
    mouse.click('left', [42, 67])
    ###点击选项数据导出，导出数据
    mouse.click('left', [1608, 11])
    time.sleep(1)
    mouse.click('left', [1655, 404])
    time.sleep(1)
    mouse.click('left', [827, 397])
    time.sleep(1)
    mouse.click('left', [1055, 547])
    time.sleep(1)
    mouse.click('left', [1110, 653])

    time.sleep(10)
    # 点击取消，完成导出
    mouse.click('left', [1016, 580])
    #沪深主要指数导出
    time.sleep(3)
    # 点击分类--》沪深主要指数，导出所有指数数据
    time.sleep(2)
    mouse.click('left', [110, 990])
    time.sleep(1)
    mouse.click('left', [120, 782])
    time.sleep(1)
    # ###点击选项数据导出，导出数据
    mouse.click('left',[1608, 11])
    time.sleep(1)
    mouse.click('left', [1655, 404])
    time.sleep(1)
    mouse.click('left', [827, 397])
    time.sleep(1)
    mouse.click('left', [1055, 547])
    time.sleep(1)
    mouse.click('left', [1110, 653])

    time.sleep(10)
    # 点击取消，完成导出
    mouse.click('left', [1016, 580])
