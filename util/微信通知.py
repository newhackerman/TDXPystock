import requests as req
import json
from wxpusher import WxPusher

class NotesToWX():

    def get_wchat_token(self,APPID,APPSECRET):
        url=f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'
        print(url)
        r=req.get(url=url)
        print(r.json()['access_token'])

    #利用139邮箱发送短信（30条/月）
    def sendmessages(self,phpnumber,message,sid):
        url=f'https://smsrebuild1.mail.10086.cn/sms/sms?func=sms:sendSms&sid={0}&rnd=0.8545016663385512&cguid=0809395694705'.format(sid)
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'cookie': 'UUIDToken=89768c89-e325-41c9-bdde-66b785cdd17a; _139_index_isSimLogin=0; _139_index_isSmsLogin=1; DEVICE_INFO_DIGEST=52a8e4e8e474755213e4540c316f8079; RMKEY=bba5e03ea551458b; cookiepartid8400=12; ut8400=2; cookiepartid=12; Login_UserNumber=13527892025; UserData={}; SkinPath28400=; rmUin8400=300533628; tipsType=1; provCode8400=1; areaCode8400=22; agentid=44e42337-35fc-4ebb-9a64-715189eeebef; pwdKey=c38b2e3e225776f1ec5dc2d6d6378f93; sid=uuid20b28c375c9b4e649cf444b12f215b06; umckey=286f1c75d8303165c17178c64ed212b4; Os_SSo_Sid=00YxODAxMzE5NDAwMDM3ODUw04BD9719000004; _139_login_version=60; loginProcessFlag=; isReadUser00YxODAxMzE5NDAwMDM3ODUw04BD9719000004=0',
        }
        data=f'<object><int name="doubleMsg">0</int><int name="submitType">1</int><string name="smsContent">{message}</string><string name="receiverNumber">86{phpnumber}</string><string name="comeFrom">104</string><int name="sendType">0</int><int name="smsType">undefined</int><int name="serialId">-1</int><int name="isShareSms">0</int><string name="sendTime"></string><string name="validImg">undefined</string><int name="groupLength">10</int><int name="isSaveRecord">1</int><int name="smsIds"></int><array name="receiverList"></array><int name="newPicture">1</int></object>'

        r=req.post(url=url,headers=headers,data=data)
        if r.json()['code']=='S_OK':
            print('短信发送成功！')
        else:
            print('短信发送失败！')


    def sendMsgToWX(self,title, content):
        url = 'http://wxpusher.zjiecode.com/api/send/message'
        payload = {
            'appToken': 'AT_cyeB3TnXCmfezmgYVy8i6Nik7ldEx6gO',
            'content': content,
            'contentType': 2,
            'topicIds':["1834"],
            'uids': ["UID_fp9wps5gWji2NK5Pk6GfHYqzjTyz"],
            'url': '',
        }
        try:
            r = req.post(url=url,  json=payload)
        except BaseException as B:
            r = req.post(url=url, json=payload)

        # print(r.json())
        if r.json()['success'] == True:
            print('通知发送成功！！')
        else:
            print('通知发送失败！！')


    def query_message(self, message_id):
        return WxPusher.query_message(message_id)

    @staticmethod
    def query_user(page, page_size, token):
        uidlist=[]
        r= WxPusher.query_user(page, page_size, token=token)
        # print(r)
        if r['success']==True:
            data=r['data']['records']
            for s in data:
                uid=s['uid']
                nickName=s['nickName']
                uidlist.append(uid)
        return uidlist
if __name__ == '__main__':
    # appID='wxdcd12c24cf91d3db'
    # appsecret='d8d76ad2586e03c896ad3ca836eb229a'
    # get_wchat_token(appID,appsecret)
    # sendmessages('13527892025', 'pythontestSend:SMS')  #非常快，但每月只有30条，不用了
    NotesToWX=NotesToWX()
    # NotesToWX.sendMsgToWX('messagetitle','messagecontent')
    appToken= 'AT_cyeB3TnXCmfezmgYVy8i6Nik7ldEx6gO'
    print(NotesToWX.query_user( 0, 100, appToken))