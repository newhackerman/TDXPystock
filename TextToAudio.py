#如果不需要保存，直接调本地的speaker 更简单【盘中语音提示】，有问题可以联系我
from gtts import gTTS   #调用的是google 翻译  
import pyttsx3
import hashlib  # md5

engine = pyttsx3.init()
def textToaAudioForgoogle(filename,text):
    if filename is None or text is None:
        return None
    tts = gTTS(text)
    tts.save(filename)

def textToaAudioForttsx3(filename,data):
    if filename is None or data is None:
        return None
    # data = '使用阿里云智能语音交互进行文字转语音             根据Aliconfig来创建一个配置文件      存放appkey accessKeyId accessKeySecret'
    md5 = hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume)  # 声音大小
    engine.setProperty('rate',130)  #每分钟读取的单词个数，数值越大，读的越快
    engine.say(data) #读出来
    engine.save_to_file(data, filename) #保存文件
    engine.runAndWait()
# #更简单的
# def wordtosay(word):
#     import speech
#     try:
#       speech.say(word)
#     except:
#         return None

if __name__ == '__main__':
    filename='./data/textToaudioTest.mp3'
    data='这是一个文本转语音的测试,this is text change to audio test ,welcome to familymeta'
    textToaAudioForttsx3(filename, data)
