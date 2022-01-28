# -*- coding: utf-8 -*-
'''集成多个浏览器到一个页面中，用于比较数据【Ex:股票行情，不同版本页面。。。】'''
import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
#
# 创建浏览器，重写重写createwindow方法实现页面连接的点击跳转
class WebEngineView(QWebEngineView):

    def __init__(self, mainwindow, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.mainwindow = mainwindow

    # 重写createwindow()
    def createWindow(self, QWebEnginePage_WebWindowType):
        # return self
        new_webview = WebEngineView(self.mainwindow)
        # new_webview = WebEngineView(self)
        self.mainwindow.create_tab(new_webview)

        return new_webview

class multiwebbrowers(QMainWindow):
    def __init__(self,url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.gridLayout=QGridLayout()
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(self)
        # 使用QToolBar创建导航栏，并使用QAction创建按钮
        # 添加导航栏
        self.navigation_bar = QToolBar('Navigation')
        # 设定图标的大小
        self.navigation_bar.setIconSize(QSize(16, 16))
        # 添加导航栏到窗口中
        self.addToolBar(self.navigation_bar)
        self.reload_button = QAction(QIcon('icons/renew.png'), '刷新', self)    

        self.navigation_bar.addAction(self.reload_button)       
        self.addwebbrowser(url)     
        self.setLayout(self.gridLayout)
     #添加浏览器
    def addwebbrowser(self,url):
        #最多显示6个窗口
        browserurlcount=len(url)
        print(browserurlcount)
        # print(url,browserurlcount)
        self.browserslist=[]
        # brows = QWebEngineView(self)
        # brows.settings()
        if browserurlcount==0:
            return
        elif  browserurlcount==1:
            for i in range(browserurlcount):
                exec("self.brows{} =None".format(i))  # 将常量变成变量
                self.browsi = QWebEngineView(self.widget)  # 一定要把browsi放在self.widget里，不然只显示一个browswer
                self.browserslist.append(self.browsi)
                self.gridLayout.addWidget(self.browserslist[i],0,i)
                self.browserslist[i].load(QUrl(url[i]))
                self.browsi.showMaximized()
        elif browserurlcount==2:
            for i in range(browserurlcount):
                exec("self.brows{} =None".format(i))  # 将常量变成变量
                self.browsi = QWebEngineView(self.widget)  # 一定要把browsi放在self.widget里，不然只显示一个browswer
                self.browserslist.append(self.browsi)
                self.browsi.setFixedSize(945, 960)
                self.gridLayout.addWidget(self.browserslist[i], 0, i)
                self.browserslist[i].load(QUrl(url[i]))
        elif browserurlcount>2  and  browserurlcount<5:
            for i in range(browserurlcount):
                exec("self.brows{} =None".format(i))  # 将常量变成变量
                self.browsi = QWebEngineView(self.widget)  # 一定要把browsi放在self.widget里，不然只显示一个browswer
                self.browserslist.append(self.browsi)
                self.browsi.setFixedSize(945, 480)
                if i<2:
                    self.gridLayout.addWidget(self.browserslist[i], 0, i)
                    self.browserslist[i].load(QUrl(url[i]))
                else:
                    self.gridLayout.addWidget(self.browserslist[i], 1, i-2)
                    self.browserslist[i].load(QUrl(url[i]))

        elif  browserurlcount>4 and browserurlcount<7:
            for i in range(browserurlcount):
                exec("self.brows{} =None".format(i))  # 将常量变成变量
                self.browsi = QWebEngineView(self.widget)  # 一定要把browsi放在self.widget里，不然只显示一个browswer
                self.browserslist.append(self.browsi)
                self.browsi.setFixedSize(945, 286)
                if i < 2:
                    self.gridLayout.addWidget(self.browserslist[i], 0, i)
                    self.browserslist[i].load(QUrl(url[i]))
                elif i>=2 and i<4:
                    self.gridLayout.addWidget(self.browserslist[i], 1, i - 2)
                    self.browserslist[i].load(QUrl(url[i]))
                elif i>=4 and i<7:
                    self.gridLayout.addWidget(self.browserslist[i], 2, int(i/2) - 2)
                    self.browserslist[i].load(QUrl(url[i]))
        else:
            for i in range(browserurlcount):
                exec("self.brows{} =None".format(i))  # 将常量变成变量
                self.browsi = QWebEngineView(self.widget)  # 一定要把browsi放在self.widget里，不然只显示一个browswer
                self.browserslist.append(self.browsi)
                self.browsi.setFixedSize(945, 312)
                if i < 2:
                    self.gridLayout.addWidget(self.browserslist[i], 0, i)
                    self.browserslist[i].load(QUrl(url[i]))
                elif i >= 2 and i < 4:
                    self.gridLayout.addWidget(self.browserslist[i], 1, i - 2)
                    self.browserslist[i].load(QUrl(url[i]))
                elif i >= 4 and i < 7:
                    self.gridLayout.addWidget(self.browserslist[i], 2, int(i / 2) - 2)
                    self.browserslist[i].load(QUrl(url[i]))
                # else:
                #     self.gridLayout.addWidget(self.browserslist[i], 2, int(i / 3) - 2)
                #     self.browserslist[i].load(QUrl(url[i]))

        self.reload_button.triggered.connect(lambda: self.brows_reload(self.browserslist))
        self.close_button.triggered.connect(lambda: self.brows_close(self.browserslist))

        self.showMaximized()

    def buttondownclicked(self):
        pass
    def buttonupclicked(self):
        pass
        # 设置窗口标题
        self.setWindowTitle('简易浏览器')
        # 设置窗口大小900*600
        self.resize(1300, 700)
        self.show()
    #刷新按钮
    def brows_reload(self,browser):
        if len(browser)>0:
            for brow in browser:
                # print(brow.objectName())
                brow.reload()
                brow.show()
    #下一页
    def brows_next(self,url):
        step=4
        urlcount=len(url)
        global position
        position+=1
        if position*step<urlcount:
            tmpurl = url[(position-1)*step:position*step]
        else:
            tmpurl = url[(position - 1) * step:urlcount]
        self.addwebbrowser(tmpurl)
        if position >= (urlcount / step):
            position = 0

    # 上一页
    def brows_last(self, url):
        step = 4
        urlcount = len(url)
        global position
        position -= 1
        if position * step <1:
            tmpurl = url[0:step]
        else:
            tmpurl = url[(position - 1) * step:position*step]
        self.addwebbrowser(tmpurl)
        if position >= (urlcount / step):
            position = 0
    #关闭
    def brows_close(self, browser):
        if len(browser) > 0:
            for brow in browser:
                brow.hide()

    # 显示地址
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.webview.setUrl(q)

    # 响应输入的地址
    def renew_urlbar(self, q):
        # 将当前网页的链接更新到地址栏
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    # 创建tab页面
    def create_tab(self, webview):
        self.tab = QWidget()
        self.tabWidget.addTab(self.tab, "新建页面")
        self.tabWidget.setCurrentWidget(self.tab)
        # 渲染到页面
        self.Layout = QHBoxLayout(self.tab)
        self.Layout.setContentsMargins(0, 0, 0, 0)
        self.Layout.addWidget(webview)

    # 关闭tab页面
    def close_Tab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)
        else:
            self.close()  # 当只有1个tab时，关闭主窗口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    url1 = 'http://www.baidu.com/'
    url2 = 'https://www.sina.com.cn/'
    url3 = 'http://www.baidu.com/'
    url4 = 'http://www.baidu.com/'
    url5 = 'https://www.sina.com.cn/'
    url6 = 'http://www.baidu.com/'
  
#     url = [url1,url2,url3,url4,url5,url6]
    url=[url1,url2,url3,url4,url5]
    childwindow = multiwebbrowers(url)
#     childwindow.setWindowTitle('行情比较')
    childwindow.show()

    sys.exit(app.exec_())
