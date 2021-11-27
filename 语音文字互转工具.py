import 语音文字转换ui
from PyQt5.Qt import *
import  sys,json,os,time,uuid,datetime
import base64,hashlib,hmac,requests
from urllib import parse
import http.client
import pyaudio,wave

from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

aliyunconfigfile='./config/aliyunconfig.json'

class AccessToken:
    @staticmethod
    def _encode_text(text):
        encoded_text = parse.quote_plus(text)
        return encoded_text.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')
    @staticmethod
    def _encode_dict(dic):
        keys = dic.keys()
        dic_sorted = [(key, dic[key]) for key in sorted(keys)]
        encoded_text = parse.urlencode(dic_sorted)
        return encoded_text.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')
    @staticmethod
    def create_token(access_key_id, access_key_secret):
        parameters = {'AccessKeyId': access_key_id,
                      'Action': 'CreateToken',
                      'Format': 'JSON',
                      'RegionId': 'cn-shanghai',
                      'SignatureMethod': 'HMAC-SHA1',
                      'SignatureNonce': str(uuid.uuid1()),
                      'SignatureVersion': '1.0',
                      'Timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                      'Version': '2019-02-28'}
        # 构造规范化的请求字符串
        query_string = AccessToken._encode_dict(parameters)
        # print('规范化的请求字符串: %s' % query_string)
        # 构造待签名字符串
        string_to_sign = 'GET' + '&' + AccessToken._encode_text('/') + '&' + AccessToken._encode_text(query_string)
        # print('待签名的字符串: %s' % string_to_sign)
        # 计算签名
        secreted_string = hmac.new(bytes(access_key_secret + '&', encoding='utf-8'),
                                   bytes(string_to_sign, encoding='utf-8'),
                                   hashlib.sha1).digest()
        signature = base64.b64encode(secreted_string)
        # print('签名: %s' % signature)
        # 进行URL编码
        signature = AccessToken._encode_text(signature)
        # print('URL编码后的签名: %s' % signature)
        # 调用服务
        full_url = 'http://nls-meta.cn-shanghai.aliyuncs.com/?Signature=%s&%s' % (signature, query_string)
        # print('url: %s' % full_url)
        # 提交HTTP GET请求
        response = requests.get(full_url)
        if response.ok:
            root_obj = response.json()
            key = 'Token'
            if key in root_obj:
                token = root_obj[key]['Id']
                expire_time = root_obj[key]['ExpireTime']
                return token, expire_time
        # print(response.text)
        return None, None
class textoraudioTransalte():
    aliyunAccessKeyID = ''
    aliyunAccessKeySecret =''
    textAppAppkey =''
    audioAppkey =''
    def __init__(self):
        self.mainwindow = QMainWindow()
        self.mainui = 语音文字转换ui.Ui_MainWindow()
        self.mainui.setupUi(self.mainwindow)  # 执行UI初始化
        self.initUI()
        self.get_config()
    def initUI(self):
        self.mainwindow.setWindowTitle('语音文字互转小工具')
        self.mainui.lineEdit_saverecordtimes.setText('20') #录音默认为20秒
        self.mainui.pushButton_saveconfig.clicked.connect(self.write_config)
        self.mainui.pushButton_openaudiofile.clicked.connect(self.openaudiofileload)
        self.mainui.pushButton_savetoaudiofile.clicked.connect(self.opensavetoaudiofile)
        self.mainui.pushButton_textToaudio.clicked.connect(self.starttextToaudio)
        self.mainui.pushButton_audioTotext.clicked.connect(self.startaudioTotext)
        self.mainui.pushButton_saverecordaudiofile.clicked.connect(self.opensavetoaudiofile)
        self.mainui.pushButton_startsaverecordaudiofile.clicked.connect(self.audio_recordaction)
    #读取配置
    def get_config(self):
        try:
            if os.path.exists(aliyunconfigfile):
                with open(aliyunconfigfile, 'r',encoding="utf-8") as f:
                    jsoncontent = json.load(f)
                    # print(jsoncontent)
                self.aliyunAccessKeyID = jsoncontent['aliyunAccessKeyID']
                self.aliyunAccessKeySecret = jsoncontent['aliyunAccessKeySecret']
                self.textAppAppkey =jsoncontent['textAppAppkey']
                self.audioAppkey = jsoncontent['audioAppkey']
                self.mainui.lineEdit_AccessKeyID.setText(self.aliyunAccessKeyID )
                self.mainui.lineEdit_AccessKeySecret.setText(self.aliyunAccessKeySecret)
                self.mainui.lineEdit_textAppAppkey.setText( self.textAppAppkey )
                self.mainui.lineEdit__audioAppkey.setText(self.audioAppkey)
                return jsoncontent
            else:
                return None
        except BaseException as b:
            print(b)
    #将配置写到文件
    def write_config(self):
        aliyunAccessKeyID=self.mainui.lineEdit_AccessKeyID.text().strip(' ')
        aliyunAccessKeySecret=self.mainui.lineEdit_AccessKeySecret.text().strip(' ')
        textAppAppkey=self.mainui.lineEdit_textAppAppkey.text().strip(' ')
        audioAppkey=self.mainui.lineEdit__audioAppkey.text().strip(' ')
        if aliyunAccessKeyID is None or aliyunAccessKeySecret is None:
            self.promptinfo('请先完成公共配置')
        jsondata={
            "aliyunAccessKeyID":aliyunAccessKeyID,
            "aliyunAccessKeySecret":aliyunAccessKeySecret,
            "textAppAppkey":textAppAppkey,
            "audioAppkey":audioAppkey
        }
        str1 = str(jsondata).replace('\'', '\"', -1)
        # print(str1)
        with open (aliyunconfigfile,'w', encoding="utf8") as fw:
            fw.write(str1)
            self.promptinfo('保存成功'+aliyunconfigfile)
    #打开文件地址
    def openaudiofileload(self):
        try:
            openfile_name ,type=QFileDialog.getOpenFileName(QWidget(),'open',r"H:\videoProcess\Audio_source")
            if openfile_name :
                self.mainui.lineEdit_openaudiofile.setText(str(openfile_name))
        except BaseException as b:
            print(b)
            return None
        # print(openfile_name)
    #打开存文件的目录
    def opensavetoaudiofile(self):
        try:
            file_path =  QFileDialog.getExistingDirectory(QWidget(),"选取文件夹",r"H:\videoProcess\Audio_source")
            self.savedir=str(file_path)
            currenttab=self.mainui.tabWidget.currentIndex()
            if currenttab ==2:
                self.mainui.lineEdit_savetoaudiofile.setText(self.savedir)
            elif  currenttab ==3:
                self.mainui.lineEdit_saverecordaudiofile.setText(self.savedir)
        except BaseException as b:
            print(b)

    def starttextToaudio(self):
        text=self.mainui.textEdit_inputtext.toPlainText()
        if str(text)=='' or text is None:
            self.promptinfo('请输入要转换的文本')
            return None
        if len(str(text))>=300:
            text=str(text)[0:299]
        filename=''
        path=self.mainui.lineEdit_savetoaudiofile.text().strip()
        format = self.mainui.comboBox_tofileExt.currentText().strip()
        print(path)
        if str(path)=='' or path is None:
            self.promptinfo('请选择目录')
            path = self.mainui.lineEdit_savetoaudiofile.text()
        tmpstr=text.replace(':','',-1).replace('/','',-1).replace('\\','',-1)
        if len(tmpstr)<10:
            filename=str(path)+'/'+ str(tmpstr)+'.'+str(format)
        else:
            filename =str(path)+'/'+ str(tmpstr[0:10])+'.'+str(format)
        token=self.get_aliyuntoken() #获取阿里云token
        if token is None:
            self.promptinfo('获取阿里云的token失败')
            return None
        textUrlencode = text
        textUrlencode = parse.quote_plus(textUrlencode)
        textUrlencode = textUrlencode.replace("+", "%20")
        textUrlencode = textUrlencode.replace("*", "%2A")
        textUrlencode = textUrlencode.replace("%7E", "~")
        sampleRate = 16000

        self.oneTextToaudio(self.textAppAppkey, token, textUrlencode, filename, format, sampleRate)

    def startaudioTotext(self):
        try:
            token = self.get_aliyuntoken()  # 获取阿里云token
            if token is None:
                self.promptinfo('获取阿里云的token失败')
                return None
            audioFile=self.mainui.lineEdit_openaudiofile.text().strip()
            result=self.audioTotext(self.audioAppkey,token, audioFile)
            self.mainui.textEdit_translateresult.setPlainText(str(result))
        except BaseException as b:
            print(b)
        self.fileTrans( self.aliyunAccessKeyID, self.aliyunAccessKeySecret, self.audioAppkey, audioFile)

    def promptinfo(self, context):
        qmessagebox = QMessageBox()
        qmessagebox.information(qmessagebox, '提示', context, QMessageBox.Yes,
                                QMessageBox.Yes)
        qmessagebox.show()
        qmessagebox.close()
    #获取阿里云token
    def get_aliyuntoken(self,):
        try:
            token, expire_time = AccessToken.create_token(self.aliyunAccessKeyID, self.aliyunAccessKeySecret)
            return token
        except BaseException as b:
            print(b)
    #文本转语音处理方法
    def oneTextToaudio(self,appKey, token, text, audioSaveFile, format, sampleRate):
        try:
            host = 'nls-gateway.cn-shanghai.aliyuncs.com'
            url = 'https://' + host + '/stream/v1/tts'
            # 设置URL请求参数
            url = url + '?appkey=' + appKey
            url = url + '&token=' + token
            url = url + '&text=' + text
            url = url + '&format=' + format
            url = url + '&sample_rate=' + str(sampleRate)
            # voice 发音人，可选，默认是xiaoyun。
            # url = url + '&voice=' + 'xiaoyun'
            # volume 音量，范围是0~100，可选，默认50。
            # url = url + '&volume=' + str(50)
            # speech_rate 语速，范围是-500~500，可选，默认是0。
            # url = url + '&speech_rate=' + str(0)
            # pitch_rate 语调，范围是-500~500，可选，默认是0。
            # url = url + '&pitch_rate=' + str(0)
            # print(url)
            # Python 2.x请使用httplib。
            # conn = httplib.HTTPSConnection(host)
            # Python 3.x请使用http.client。
            conn = http.client.HTTPSConnection(host)
            conn.request(method='GET', url=url)
            # 处理服务端返回的响应。
            response = conn.getresponse()
            # print('Response status and response reason:')
            # print(response.status ,response.reason)
            contentType = response.getheader('Content-Type')
            # print(contentType)
            body = response.read()
            if 'audio/mpeg' == contentType:
                with open(audioSaveFile, mode='wb') as f:
                    f.write(body)
                print('The GET request succeed!')
                self.promptinfo('转换成功!')
            else:
                print('The GET request failed: ' + str(body))
                self.promptinfo('转换失败!'+ str(body))
            conn.close()
        except BaseException as b:
            print(b)
    #语音转文本
    def audioTotext(self,appKey,token, audioFile):
        # 服务请求地址
        url = 'https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/asr'

        # format = 'mp3'
        # format = 'wav'
        format = 'pcm'
        sampleRate = 16000
        enablePunctuationPrediction = True
        enableInverseTextNormalization = True
        enableVoiceDetection = False
        enable_intermediate_result=False #是否返回中间结果
        # 设置RESTful请求参数
        request = url + '?appkey=' + appKey
        request = request + '&format=' + format
        request = request + '&sample_rate=' + str(sampleRate)

        if enablePunctuationPrediction:
            request = request + '&enable_punctuation_prediction=' + 'true'

        if enableInverseTextNormalization:
            request = request + '&enable_inverse_text_normalization=' + 'true'

        if enableVoiceDetection:
            request = request + '&enable_voice_detection=' + 'true'
        if enable_intermediate_result:
            request = request + '&enable_intermediate_result=' + 'true'

        # print('Request: ' + request)
        # 读取音频文件
        with open(audioFile, mode='rb') as f:
            audioContent = f.read()

        host = 'nls-gateway.cn-shanghai.aliyuncs.com'

        # 设置HTTPS请求头部
        httpHeaders = {
            'X-NLS-Token': token,
            'Content-type': 'application/octet-stream',
            'Content-Length': len(audioContent)
        }
        # print(httpHeaders)
        # print(token)
        conn = http.client.HTTPConnection(host)
        conn.request(method='POST', url=request, body=audioContent, headers=httpHeaders)
        response = conn.getresponse()
        # print('Response status and response reason:')
        # print(response.status, response.reason)
        if response.status == 400:
            print(response.reason)
            return None
        body = response.read()
        # print('body:', body)
        try:
            # print('Recognize response is:')
            body = json.loads(body)
            # print(body)

            status = body['status']
            if status == 20000000:
                result = body['result']
                print('Recognize result: ' + result)
                return str(result)
                # self.mainui.textEdit_translateresult.setText(str(result))
            else:
                # self.promptinfo('语音转文本失败')
                return 'error'
                print('Recognizer failed!')

        except ValueError:
            print('The response is not json format string')
            return 'error'
        conn.close()
    #调sdk 语音转文本（filelink必需存储在阿里云上）
    def fileTrans(self,akId, akSecret, appKey, fileLink) :
        # 地域ID，固定值。
        REGION_ID = "cn-shanghai"
        PRODUCT = "nls-filetrans"
        DOMAIN = "filetrans.cn-shanghai.aliyuncs.com"
        API_VERSION = "2018-08-17"
        POST_REQUEST_ACTION = "SubmitTask"
        GET_REQUEST_ACTION = "GetTaskResult"
        # 请求参数
        KEY_APP_KEY = "appkey"
        KEY_FILE_LINK = "file_link"
        KEY_VERSION = "version"
        KEY_ENABLE_WORDS = "enable_words"
        # 是否开启智能分轨
        KEY_AUTO_SPLIT = "auto_split"
        # 响应参数
        KEY_TASK = "Task"
        KEY_TASK_ID = "TaskId"
        KEY_STATUS_TEXT = "StatusText"
        KEY_RESULT = "Result"
        # 状态值
        STATUS_SUCCESS = "SUCCESS"
        STATUS_RUNNING = "RUNNING"
        STATUS_QUEUEING = "QUEUEING"
        # 创建AcsClient实例
        client = AcsClient(akId, akSecret, REGION_ID)
        # 提交录音文件识别请求
        postRequest = CommonRequest()
        postRequest.set_domain(DOMAIN)
        postRequest.set_version(API_VERSION)
        postRequest.set_product(PRODUCT)
        postRequest.set_action_name(POST_REQUEST_ACTION)
        postRequest.set_method('POST')
        # 新接入请使用4.0版本，已接入（默认2.0）如需维持现状，请注释掉该参数设置。
        # 设置是否输出词信息，默认为false，开启时需要设置version为4.0。
        task = {KEY_APP_KEY : appKey, KEY_FILE_LINK : fileLink, KEY_VERSION : "4.0", KEY_ENABLE_WORDS : False}
        # 开启智能分轨，如果开启智能分轨，task中设置KEY_AUTO_SPLIT为True。
        # task = {KEY_APP_KEY : appKey, KEY_FILE_LINK : fileLink, KEY_VERSION : "4.0", KEY_ENABLE_WORDS : False, KEY_AUTO_SPLIT : True}
        task = json.dumps(task)
        print(task)
        postRequest.add_body_params(KEY_TASK, task)
        taskId = ""
        try :
            postResponse = client.do_action_with_exception(postRequest)
            postResponse = json.loads(postResponse)
            print (postResponse)
            statusText = postResponse[KEY_STATUS_TEXT]
            if statusText == STATUS_SUCCESS :
                print ("录音文件识别请求成功响应！")
                taskId = postResponse[KEY_TASK_ID]
            else :
                print ("录音文件识别请求失败！")
                return
        except ServerException as e:
            print (e)
        except ClientException as e:
            print (e)
        # 创建CommonRequest，设置任务ID。
        getRequest = CommonRequest()
        getRequest.set_domain(DOMAIN)
        getRequest.set_version(API_VERSION)
        getRequest.set_product(PRODUCT)
        getRequest.set_action_name(GET_REQUEST_ACTION)
        getRequest.set_method('GET')
        getRequest.add_query_param(KEY_TASK_ID, taskId)
        # 提交录音文件识别结果查询请求
        # 以轮询的方式进行识别结果的查询，直到服务端返回的状态描述符为"SUCCESS"、"SUCCESS_WITH_NO_VALID_FRAGMENT"，
        # 或者为错误描述，则结束轮询。
        statusText = ""
        while True :
            try :
                getResponse = client.do_action_with_exception(getRequest)
                getResponse = json.loads(getResponse)
                print (getResponse)
                statusText = getResponse[KEY_STATUS_TEXT]
                if statusText == STATUS_RUNNING or statusText == STATUS_QUEUEING :
                    # 继续轮询
                    time.sleep(3)
                else :
                    # 退出轮询
                    break
            except ServerException as e:
                print (e)
            except ClientException as e:
                print (e)
        if statusText == STATUS_SUCCESS :
            return getResponse
            print ("录音文件识别成功！")
        else :
            print ("录音文件识别失败！")
            return None
        return getResponse
    #录音按钮事件
    def audio_recordaction(self):
        times=self.mainui.lineEdit_saverecordtimes.text().strip()

        if times.isalpha() or str(times)=='':
            self.promptinfo('请输入正确的录音时间秒数，为数字')
            return
        path1=self.mainui.lineEdit_saverecordaudiofile.text().strip()
        if str(path1)=='':
            self.promptinfo('请选择要保存的目录')
            return
        self.promptinfo('2秒后开始')
        time.sleep(1)
        self.audio_record(times,path1)
    #录音功能
    def audio_record(self,times,path1):
        times=int(times)
        CHUNK = 1024  # 每个缓冲区的帧数
        FORMAT = pyaudio.paInt16  # 采样位数
        CHANNELS = 1  # 单声道
        RATE = 16000  # 采样率
        # '''RATE表示采样率，常用的采样率有：8000, 16000, 22050, 44100, 48000和 96000 Hz'''
        timenow=str(datetime.datetime.now().strftime('%H_%M_%S'))
        filename=str(path1)+'/'+'voice_record_start_'+timenow+'.mp3'
        try:
            self.start_timer(times, 1000) #开始倒计时
            """ 录音功能 """
            p = pyaudio.PyAudio()  # 实例化对象
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)  # 打开流，传入响应参数
            wf = wave.open(filename, 'wb')  # 打开 wav 文件。
            wf.setnchannels(CHANNELS)  # 设置单声道
            wf.setsampwidth(p.get_sample_size(FORMAT))  # 设置采样位宽为16bits
            wf.setframerate(RATE)  # 设置采样率

            print('Start speaking for %ds\n' % times)

            for _ in range(0, int(RATE * times / CHUNK)):
                data = stream.read(CHUNK)
                wf.writeframes(data)  # 写入数据
            stream.stop_stream()
            stream.close()
            print('End of Recording.')
            p.terminate()
            wf.close()
        except BaseException as b:
            print(b)
            return
    #倒计时
    def start_timer(self, count=20, interval=1000):
        counter = 0
        count=int(count)
        # print(count)
        self.mainui.pushButton_startsaverecordaudiofile.setDisabled(True)
        def handler():
            nonlocal counter
            counter += 1
            self.mainui.label_times.setText('倒计时：'+str(int(count)-int(counter))) #改变计时器的显示
            if counter >= count:
                timer.stop()
                timer.deleteLater()
                self.mainui.pushButton_startsaverecordaudiofile.setDisabled(False)

        timer = QTimer()
        timer.timeout.connect(handler)
        timer.start(interval)

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        transalte = textoraudioTransalte()
        transalte.mainwindow.show()

        app.exec()
        sys.exit()
    except BaseException as b :
        print(b)
        sys.exit(1)
