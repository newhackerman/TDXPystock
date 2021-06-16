import requests

class aiwencai():
    def __init__(self):
        # self.chrome_option = webdriver.ChromeOptions()
        # self.chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 允许开发者模式
        # # headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        # #     }
        # # #self.chrome_option.add_argument('--headless')
        # # self.chrome_option.add_argument(headers)
        # #self.chrome_option.add_argument('--disable-gpu')
        # self.brow=webdriver.Chrome(executable_path='../chromedriver.exe', options=self.chrome_option)
        # # self.brow.execute_script(
        # #     'Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) ')  # 将属性设置为非webdriver 方式，（淘宝针对这个有反爬机制）

        pass

    def questions(self,question):
        r=''
        url='http://www.iwencai.com/unifiedwap/unified-wap/v2/result/get-robot-data'
        # self.brow.get(url)
        # q=self.brow.find_element_by_class_name('search-input').send_keys(question)
        # click=self.brow.find_element_by_class_name('search-icon').click()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'Cookie': 'searchGuide=sg; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1608770907,1609917926,1610114215,1611192209; reviewJump=nojump; usersurvey=1; v=A-xOcNJfoJFX0bSt1GiqynybvcEdpZBLkkmkE0Yt-Bc6UYL3brVg3-JZdKSV',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'basic.10jqka.com.cn'
            }
        data='question='+ str(question.encode("utf-8"))+'&perpage=5000&page=1&secondary_intent=&log_info={"input_type":"click"}'
        print(data)
        req=requests.session()

        req.headers=headers
        try:
            r=req.post(url=url,data=data,timeout=5)
            print(r.text)
        except BaseException as b:
            print(b)
        result=r.text
        print(result)

    def format(self):
        pass

if __name__ == '__main__':
    awencai=aiwencai()
    awencai.questions('机构持股大于5%')



