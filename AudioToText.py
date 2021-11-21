#  使用百度api 语音转文字功能 [对源语音要求太高了] 本文件代码运行有问题不要联系我，告诉你环境问题，整这个环境很花时间，一时半会根本说不清，自行google搜索解决
import requests as req
import json,base64,os
import speech_recognition as sr
from pocketsphinx import AudioFile
from Speech_and_Text import speech_to_text_cmu
import ffmpeg

baiduaudioappapiid='xxx' #文字转语音的apiid
baiduaudioappAPI_Key='xxx'
baiduaudioappSecret_Key='xxx'
#获取百度对应的appid的token
def getbaiduApiToken(grant_type,API_Key,Secret_Key):
    try:
        host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_Key}&client_secret={Secret_Key}'
        response = req.get(host)
        if response:
            return response.json()['access_token']
    except BaseException as b:
        print(b)
        return None           #wg
#使用百度的语音识别
def audioTotextForBaidu(audiofile):
    try:
        if os.path.exists(audiofile):
            pass
        else:
            return None

        token=getbaiduApiToken('client_credentials',baiduaudioappAPI_Key,baiduaudioappSecret_Key)
        if token is None:
            return None
        print(token)
        filetext=''

        with open(audiofile,'rb') as fr:
            filetext = fr.read() #将读取的二进制内容转成base64

        filelen = len(filetext)
        base64text=base64.b64encode(filetext)
        if str(base64text).strip() =='' or base64text is None:
            return None

        url='http://vop.baidu.com/server_api'
        header={'Content-Type':'application/json'}
        postdata={
        "format":"pcm",
        "rate":16000,
        #"dev_pid":1537,
        "channel":1,
        "token":token,
        "cuid":'baidu_workshop', #用户唯一标识
        "len":filelen,
        "speech":base64text,
        }
        response=req.post(url=url,json=postdata,headers=header,timeout=60)
        result=response.json()['result']
        print(result)
        return result
    except BaseException as b :
        print(b)
        return b
 #使用本地安装的speech_recognition 语音包[PocketSphinx]
def audioTotextForlocal_zh_CN(audiofile):
    try:
        r = sr.Recognizer()
        # print(r)
        wavFile = sr.AudioFile(audiofile)
        # print(wavFile)
        with wavFile as source:
            audio = r.record(source)

        # recognize speech using Sphinx
        try:
            return r.recognize_sphinx(audio, language="zh-CN")
        except sr.UnknownValueError:
            print("无法理解")
        except sr.RequestError as e:
            print("error; {0}".format(e))
    except BaseException as b:
        print(b)
    # print("听起来像英文 " + r.recognize_sphinx(audio))
 #使用本地安装的speech_recognition 语音包[PocketSphinx]
def audioTotextForlocal_en_US(audiofile): #使用本地安装的speech_recognition 语音包[PocketSphinx]
    try:
        r = sr.Recognizer()
        # print(r)
        wavFile = sr.AudioFile(audiofile)
        # print(wavFile)
        with wavFile as source:
            audio = r.record(source)
        # recognize speech using Sphinx
        try:
           return r.recognize_sphinx(audio, language="en-US")
        except sr.UnknownValueError:
            print("无法理解")
        except sr.RequestError as e:
            print("error; {0}".format(e))
    except BaseException as b:
        print(b)

#调用科大讯飞
def audioTotext_by_ifly():
    from Speech_and_Text import speech_to_text_ifly
    # 从文件读入
    # speech_to_text_ifly(audio_path="path_of_audio", if_microphone=False)
    # 从麦克风读入
    speech_to_text_ifly(if_microphone=True)
#从麦克风读取声音转文字
def frommkaudiotoText_by_cmu(filename):

    # 从文件读入
    speech_to_text_cmu(audio_path=filename, if_microphone=False)
    # 从麦克风读入
    # speech_to_text_cmu(if_microphone=True)
#采样率转换 也达到压缩的效果
def cylchange(srcfile,targetfile,cyl):
    try:
        ffmpeg.input(srcfile).output(targetfile, ar=cyl).run()
    except BaseException as b:
        print(b)
        return None
#本地语音文件float数据 转int
def local_audiofile_OnFloatToInt(srcfile):
    pass

if __name__ == '__main__':

    # audiofile_cn=u'./data/textToaudioTest.mp3'
    audiofile_cn=u'./data/test.wav'
    audiofile_en=u'./data/testfile.mp3'
    # audioTotextForBaidu(audiofile_cn)
    sample_rate=25050
    print(audioTotextForlocal_zh_CN(audiofile_cn))
    targetfile=u'./data/testfile'+str(sample_rate)+'.mp3'
    cylchange(audiofile_en,targetfile,sample_rate)
    print(audioTotextForlocal_en_US(audiofile_cn))

    # frommkaudiotoText_by_cmu(audiofile_en)

