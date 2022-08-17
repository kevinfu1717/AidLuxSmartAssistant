# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 13:40:32 2022

@author: kevin
"""
import feishuTools 
import queue
import utils
def debugPrint(msg,outputer,processer=None):
    print('debugPrint',msg)
def record(msg,outputer,processer=None):
    # print('record',msg)
    if "宝宝" or "肉肉" in msg:
        person="宝宝"
    elif "妈妈" in msg:
        person="妈妈"
    else:
        person=""
    
    if utils.punc(msg,0):
        msg=msg[1:]
    # print('record', msg)
    resultDict=processer.run(msg)
    _,content=feishuTools.addProcess(query="",content=msg,startTimeStr=resultDict['startTime'],endTimeStr=resultDict['endTime'],
                                     person=person,memo="")
        
    outputer.speak(content)
    return content

strategyDict={'记录':record,'测试':debugPrint}
