
import time
import requests
import header
import json
import datetime
class NerClass():
    def __init__(self,method='online',logger=None):
        self.logger=logger
        self.print('ner class init')
        self.parseTime=eval('self.'+method+'ParseTime')
        if method=='local':
            import jionlp as jio
    def print(self,text):
        if self.logger is None:
            print('print text',text)
        else:
            self.logger.debug(text)

    def run(self,text):

        t1,t2=self.parseTime(text)
        resultDict={'startTime':t1,"endTime":t2}
        return resultDict
    def onlineParseTime(self,text):
        try:
            jsonData={"query":text}
            rr=requests.post(header.nerUrl,json=jsonData)
            jsonReply=json.loads(rr.text)
            self.print(jsonReply)

            time1=jsonReply['data']['startTime']
            time2=jsonReply['data']['endTime']
        except:
            time1=''
            time2=''
        return time1,time2
    def timeCheck(self,dateTimeStr):
        local_format = r'%Y-%m-%d %H:%M:%S'
        try:
            # local_format = r'%Y-%m-%dT%H:%M:%S'
            msTime = datetime.datetime.strptime(dateTimeStr, local_format)
            return dateTimeStr
        except:
            return  ''
    def localParseTime(self,text):
        try:
            result=jio.parse_time(text,time_base=time.time())

            # text="小太阳记录宝宝在半小时前开始吃奶。小太阳记录，妈妈准备洗澡。"
            # print(jio.parse_time(text, time_base=time.time()))
            # {'type': 'time_point', 'definition': 'accurate', 'time': ['2022-03-17 13:07:00', '2022-03-17 13:37:28']}
            time1=result['time'][0]#begin time
            time2=result['time'][1]#end time
            #
            time1=self.timeCheck(time1)
            time2=self.timeCheck(time2)

            self.print('ner time:'+str(time1)+' to '+str(time2))
        except:
            time1=''
            time2=''

        return time1,time2

if __name__=='__main__':
    text = "小太阳记录宝宝在11点之前开始吸母乳，肠胃。小太阳记录，妈妈准备洗澡。"
    nc=NerClass(method='online')
    print('result',nc.run(text))
# words = jiagu.seg(text) # 分词
# print(words)
# pos = jiagu.pos(words) # 词性标注
# print(pos)
#
# ner = jiagu.ner(words) # 命名实体识别
# print(ner)
