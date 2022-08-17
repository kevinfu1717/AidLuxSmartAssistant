# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 11:09:54 2022

@author: kevin
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 11:19:31 2022

@author: kevin
"""

from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
from pywebio import start_server
import queue
from header import queryUrl
#import moduleInput,moduleOutput
import requests
#from moduleManager import *
from strategy import *
import json

def inputerrun(data):
    
    data={"msg": data,
        }
    
    
    rr=requests.post(queryUrl,json=data)
    
    data=json.loads(rr.text)
    if data['result_code']!='success':
        
        print(data)
#    print(data)
def testFunc():
    
    ss='小太阳帮我记录宝宝1点已经吃人奶瓶喂'
    inputerrun(ss)
    
def inputFunc():
    # input的合法性校验
    # 自定义校验函数

    def check_validate(n):
        pass

    # myAge = input('点击输入框进行语音输入', type=TEXT, validate=None, help_text='点击输入框进行语音输入',onchange=inputChange)
    myTxt = textarea(label='点击输入框进行语音输入', rows=3,
                     type=TEXT, validate=None, help_text='点击输入框进行语音输入', 
                     onchange=inputerrun)
#
#    put_textarea(im.newMsg)

    
    
if __name__ == '__main__':
#    testFunc()
    
    start_server(
        applications=[inputFunc, ],
        debug=True,
        port=3086,
        auto_open_webbrowser=True,
        remote_access=False,
    )
#    
#    cm.join()