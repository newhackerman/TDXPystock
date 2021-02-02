import requests
from selenium import webdriver

class aiwencai():
    def __init__(self):
        self.chrome_option = webdriver.ChromeOptions()
        self.chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 允许开发者模式
        # headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        #     }
        # #self.chrome_option.add_argument('--headless')
        # self.chrome_option.add_argument(headers)
        #self.chrome_option.add_argument('--disable-gpu')
        self.brow=webdriver.Chrome(executable_path='../chromedriver.exe', options=self.chrome_option)
        self.brow.execute_script(
            'Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) ')  # 将属性设置为非webdriver 方式，（淘宝针对这个有反爬机制）

        pass

    def questions(self,question):
        url='http://www.iwencai.com/unifiedwap/home/index?sign=1612252037820'
        self.brow.get(url)
        q=self.brow.find_element_by_class_name('search-input').send_keys(question)
        click=self.brow.find_element_by_class_name('search-icon').click()


    def format(self):
        pass

if __name__ == '__main__':
    awencai=aiwencai()
    awencai.questions('高瓴资本持股')


