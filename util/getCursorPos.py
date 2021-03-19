import win32api
import time
import ctypes
#每隔3秒输出当前鼠标的位置坐标

def GetCursorPos():
    #在win10上的高清屏上获取不到正确的坐标，下面两行是进行初始化的
    awareness = ctypes.c_int()
    ctypes.windll.shcore.SetProcessDpiAwareness(2)   #如果2不行，换1，0试试
    while True:
        print(win32api.GetCursorPos())
        time.sleep(3)


class PROCESS_DPI_AWARENESS() :
    PROCESS_DPI_UNAWARE = 0
    PROCESS_SYSTEM_DPI_AWARE = 1
    PROCESS_PER_MONITOR_DPI_AWARE = 2



if __name__ == '__main__':
    GetCursorPos()