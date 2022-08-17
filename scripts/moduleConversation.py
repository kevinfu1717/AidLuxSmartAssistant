# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 13:24:32 2022

@author: kevin
"""

import string
import time
import queue
import utils
import threading
ChinesePunc = ["，", "。", "、", "？", "！"]


class converManager(threading.Thread):
    def __init__(self,msgQueue,stateTimeQueue,strategyDict,outputer=None,processer=None,
                 wuWordList=['小太阳','太阳'],duplex=False,logger=None):
        
        super(converManager, self).__init__()

        self.msgQueue=msgQueue
        self.runFlag=True
        self.logger=logger
        self.stateTimeQueue=stateTimeQueue
        self.wuWordList=wuWordList
        self.strategyDict=strategyDict
        self.wuWordRange=2
        self.outputer=outputer
        self.processer=processer
        print('init conversation manager', self.wuWordList)
    def run(self):
        self.print('cm start to run')
        while self.runFlag:
            realMsg=self.wakeupProcess()
            
            if len(realMsg)>0:
                
                self.converProcess(realMsg)
            else:
                time.sleep(0.2)
    def print(self,strData):
        if self.logger is None:
            print(str(strData))
        else:
            self.logger.debug(str(strData))
                
    def wakeupProcess(self):
        realMsg=""
#        print('self.msgQueue',self.msgQueue.qsize())
        if not self.msgQueue.empty():
            newMsg=self.msgQueue.get()
#            print(newMsg,'get')
            for wuWord in self.wuWordList:
                wuWordIndex=newMsg.find(wuWord)
                self.print('wuWordIndex'+str(wuWordIndex)+str(wuWord))
                if wuWordIndex>=0 and wuWordIndex<self.wuWordRange:
                    #wake up word come
                    realMsg=newMsg[wuWordIndex+len(wuWord):]
                    
                    self.print('wake up with:'+str(realMsg))
                    try:
                        self.outputer.toast(realMsg)
                    except:
                        pass
                    break
        return realMsg

        
    def converProcess(self,realMsg):
        for key,value in  self.strategyDict.items():
            ## which strategy to use
            strategyResult=utils.strategyChoose(key,realMsg)
            
            self.print(str(key)+str(realMsg)+'strategyResult'+str(strategyResult))
            if strategyResult>=0:
                #do strategy
                # self.print('strategyResult'+str(strategyResult)+str(value))
                result=value(realMsg[strategyResult+len(key):],self.outputer,self.processer)
                
                if result is not None:
                    self.print(result)
                break
             
if __name__=='__main__':
    mq=queue.Queue()
    sq=queue.Queue()
    iq=queue.Queue()
    import moduleInput,moduleOutput,moduleProcesser
    ss='小太阳帮我记录宝宝1点已经吃人奶瓶喂'
#    mq.put('小太阳帮我记录宝宝1点已经吃人奶瓶喂')
    iq = queue.Queue()
    import moduleOutput

    #    ss='小太阳帮我记录宝宝1点已经吃人奶瓶喂'
    iq.put(['小太阳记录宝宝1点已经吃人奶瓶喂'])

    from strategy import *

    log=None
    duplex = False
    inp = moduleInput.inputClass(mq, sq, iq, duplex=duplex, logger=log)
    processer=moduleProcesser.processerClass(logger=log)
    ouputer = moduleOutput.outputManager(sq, logger=log)

    cm = converManager(mq, sq, strategyDict, ouputer, processer,duplex=duplex, logger=log)

    cm.daemon = True
    inp.start()
    cm.start()