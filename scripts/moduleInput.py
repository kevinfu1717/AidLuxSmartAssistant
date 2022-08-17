# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 09:19:23 2022

@author: kevin
"""


import string
import time
import threading
import utils
class inputClass(threading.Thread):
    def __init__(self,msgQueue,stateTimeQueue,inputQueue,duplex=False,logger=None):
        
        super(inputClass, self).__init__()
        self.allData = ""
        self.newMsg = ""
        
        self.grepSoundTimeThreshold = 5
        self.msgQueue=msgQueue
        self.stateTimeQueue=stateTimeQueue
        self.setState(0)
        self.duplex=duplex
        self.inputQueue=inputQueue
        self.runFlag=True
        self.logger=logger
        print("init finish: inputer stateTimeQueue:",self.stateTimeQueue.qsize())

    def setState(self,stateValue):
        self.state=stateValue
        self.stateTimeQueue.put(self.state)
    def timeOutCheck(self, threshold, stateTime):
        if time.time() - stateTime > threshold:
            self.setState(0)
            self.print('state0 timeout')

    def processMsg(self, newMsg):
        print('processMsg',newMsg,self.duplex)
        if not self.duplex:
            if self.allData!="":
                self.state=self.stateTimeQueue.get()
                self.print('minput'+str(self.state))
                self.timeOutCheck(self.grepSoundTimeThreshold, self.state)
                self.print('minput2'+str(self.state))
            
            if self.state != 0:
                
                self.setState(0)
                self.print('state 0: ignore 1 sentences')
                return
        
        self.newMsg = newMsg     
        self.print(('newmsg add:'+str(self.newMsg)+'alldata num:'+str(len(self.allData))))
        self.msgQueue.put(newMsg)
#            droid.toast(self.newMsg)
#            self.speak(self.newMsg)
    def preProcess(self,newMsg):
        ## replace first  punctuation
        if utils.punc(newMsg,0):
            newMsg = newMsg[1:]
        return newMsg
    
    def run(self):
        while self.runFlag:
            dataArray=self.inputQueue.get()
            #self.print('module input dataArray:'+str(data))
            data=dataArray[0]
            self.chiefProcess(data)
            
    def chiefProcess(self, data):
        #self.print('data'+str(data)+',alldata:'+str(len(self.allData)))
        self.newMsg = ""
        allDataLen=len(self.allData)
        if len(data) > allDataLen and allDataLen>0:

            newMsg = data[allDataLen:]
#            print('nnn',newMsg)
            ## not just a word
            if len(newMsg) > 1:
                ## newMsg为最新说话内容
                newMsg = self.preProcess(newMsg)
                self.processMsg(newMsg)
        ## allData为文本框中所有内容
        self.allData = data
    def print(self,strData):
        if self.logger is None:
            print(str(strData))
        else:
            self.logger.debug(str(strData))
if __name__=='__main__':
    import queue
    mq=queue.Queue()
    sq=queue.Queue()
    iq=queue.Queue()
    import moduleOutput
#    ss='小太阳帮我记录宝宝1点已经吃人奶瓶喂'
    iq.put('小太阳帮我记录宝宝1点已经吃人奶瓶喂')
    inputer=inputClass(mq,sq,iq)
    
#    om=moduleOutput.outputManager(sq)
#    from strategy import *
#    cm=converManager(mq,sq,strategyDict,None)
    inputer.start()
    print(mq.qsize())
    