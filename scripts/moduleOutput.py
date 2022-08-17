# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 09:37:41 2022

@author: kevin
"""
import time
import threading
try:
    import android
    droid = android.Android()
except:
    droid=None
class outputManager():
    def __init__(self,stateTimeQueue,duplex=False,logger=None):
        
        
        self.stateTimeQueue=stateTimeQueue
        self.duplex=duplex
        self.logger=logger
        print('init outputManager duplex',duplex)
    def setState(self,stateValue):
        self.state=stateValue
        self.stateTimeQueue.put(self.state)
    def print(self,strData):
        if self.logger is None:
            print(str(strData))
        else:
            self.logger.debug(str(strData))
    def speak(self, content):
        if not self.duplex:
            self.stateTimeQueue.get(block=True)
            
            self.setState(time.time())
            self.print('output change state say'+str(self.state))
            
        
        try:
            droid.ttsSpeak(content)
            self.print('speak'+"content")
        except Exception as e:
            self.print('speak fail'+str(content)+str(e))
            pass
    def toast(self, content):
        
        try:
            droid.makeToast( content)
            self.print('toast'+str(content))
        except Exception as e:
            self.print('toast fail'+str(content)+str(e))
            pass