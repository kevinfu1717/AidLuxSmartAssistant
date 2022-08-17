# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 13:55:42 2022

@author: kevin
"""

import traceback
import json
import requests
import time
from header import *
import re
import datetime

import os


import re
import utils
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

def checkHeader(jsonData,acceptDelayMS=3000):
    data=''
    try:
        header=jsonData['header']
        create_time=int(header['create_time'])
        nowMS=time.time()*1000
        print('delay',nowMS-create_time,'threshold',acceptDelayMS,nowMS-create_time<acceptDelayMS)
        if nowMS-create_time<acceptDelayMS:
            
            return True
    except Exception as e:
        traceback.print_exc()
    return False

## 时区为utc的问题解决：
os.environ['TZ'] = 'Asia/Shanghai'
def addProcess(query="",content="",startTimeStr='',endTimeStr='',person="",memo=""):
    app_token=baseDict["base1"]
    ##
    table_id=tableDict['base1total']
    
    return addBaseRecord(appHeader,app_token,table_id,content,startTimeStr,endTimeStr,person,memo)

def addBaseRecord(appHeader,app_token,table_id,content="",startTimeStr='',endTimeStr='',person="",memo=""):
    record_id=""
    #print('add base record:',content)
    if len(content)>0:
        
        app_id=appHeader.app_id
        app_secret=appHeader.app_secret
        #print('app_id',app_id)
        token=getTenantToken(app_id,app_secret)
        #print('token',token)
        headers={'Authorization': 'Bearer {}'.format(token),
            "Content-Type":"application/json; charset=utf-8"}
        url="https://open.feishu.cn/open-apis/bitable/v1/apps/"+app_token+"/tables/"+table_id+"/records"
        #content=json.dumps({"text":"Tom test content"})
        #title,save_url=saveClip(data_url)
        
        startTime=utils.formatTime(startTimeStr)
        endTime=utils.formatTime(startTimeStr)
        fieldDict={
                "开始时间": startTime,
                "结束时间": endTime,
                "人物":person,
                "事项":content,
                "创建时间":int(time.time() * 1000),
                "备注":memo, 
        }
        if 1==0:
            fieldDict.update(          
                {"文档":{
                      "text": "title",
                      "link": "save_url",
                }}
            )
        replyDict={"fields":fieldDict}
        print('send feishu post:',replyDict)
        rr=requests.post(url,json=replyDict,headers=headers)
        print('rr==',rr.text)
        dataJson=json.loads(rr.text)
        try:
            data=dataJson['data']
            record=data['record']
            record_id=record['record_id']
            content=record['fields']['事项']
        except Exception as e:
            traceback.print_exc()
        # print('record_id',record_id)
    return record_id,content
def sendMsg(appHeader,message_id,data_send="data got"):

    app_id=appHeader.app_id
    app_secret=appHeader.app_secret

    token=getTenantToken(app_id,app_secret)

    content=json.dumps({"text":data_send})

    replyDict= {
    "content": content,
    "msg_type": "text"
    }
    
    headers={'Authorization': 'Bearer {}'.format(token),
        "Content-Type":"application/json; charset=utf-8"}
    url="https://open.feishu.cn/open-apis/im/v1/messages/"+message_id+"/reply"
    rr=requests.post(url,json=replyDict,headers=headers)
    print('rr==',rr.text)

def updateRecord(data_url,appHeader,app_token,table_id,record_id):
    url=saveClipUrl
    replyDict={"data_url":data_url,
                "app_id":appHeader.app_id,
                "app_secret":appHeader.app_secret,
                "app_token":app_token,
                "table_id":table_id,
                "record_id":record_id}
    rr=requests.post(url,json=replyDict)
    print('saveClip',rr.text)
    return

