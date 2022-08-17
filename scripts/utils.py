# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 17:21:58 2022

@author: kevin
"""
import string
import traceback
import json
import requests
import time
import datetime
import re
import os
## 时区为utc的问题解决：
os.environ['TZ'] = 'Asia/Shanghai'
ChinesePunc = ["，", "。", "、", "？", "！"]
def getData(jsonData):
    data=''
    try:
        event=jsonData['event']
        sender=event['sender']
    except Exception as e:
        traceback.print_exc()

    try:
        message=event['message']
        chat_id=message['chat_id']
        message_id=message['message_id']
        message_type=message['message_type']
    except Exception as e:
        traceback.print_exc()

    try:
        content=message['content']
        content=json.loads(content)
        data=content[message_type]
    except Exception as e:
        traceback.print_exc()

    try:
        tenant_key=sender['tenant_key']
    except Exception as e:
        traceback.print_exc()

    return data,message_id

def getTenantToken(app_id,app_secret):
    data={"app_id": app_id,
        "app_secret":app_secret
        }
    url="https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    
    rr=requests.post(url,json=data)
    print(rr.text)
    data=json.loads(rr.text)
    return data['tenant_access_token']
def getUrl(dataStr):
    url=""
    dataArray=dataStr.split(" ")
    for data in dataArray:
        if "http" in data:
            url="http"+data.split("http")[1]
            break
    return url
def punc(text,index):
    if text[index] in string.punctuation or text[index] in ChinesePunc:
        return True
    else:
        return False
def getTitle(url):
    html=requests.get(url)
    title=""
    if html.status_code == 200:
        html_bytes=html.content
        html_str=html_bytes.decode()
        print('html_str',html_str)
        titleList=re.findall(r"<title>(.+?)</title>", html_str)
        print('titleList',titleList)
        if len(titleList)>0:
            title=titleList[0]
    return title

            
                
            
def strategyChoose(key,msg,regRange=3):
    ii=msg.find(key)
    print('strategy key',key,msg,ii)
    if ii>=0 and ii<regRange:
        
        print('strategy key',key,msg,ii)
        return ii
    else:
        return -1

def formatTime(dateTimeStr,local_format = r'%Y-%m-%d %H:%M:%S'):
    nowTime = int(time.time() * 1000)
    msTime = nowTime
    if len(dateTimeStr) > 0:
        try:

            # local_format = r'%Y-%m-%dT%H:%M:%S'
            msTime = datetime.datetime.strptime(dateTimeStr, local_format)
            msTime = int(time.mktime(msTime.timetuple()) * 1000)
        except:
            pass
    # print(type(dateTimeStr), dateTimeStr)

    return msTime


if __name__=='__main__':
    strategyChoose('记录','小太阳记录宝宝晒太阳小太阳记录宝宝晒太阳key,realMs')
