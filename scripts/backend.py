from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
import json

import sys
import traceback
from multiprocessing import Queue

#import queue

import moduleInput,moduleOutput
import moduleConversation
import moduleProcesser
from strategy import *


##
from logging import getLogger, INFO
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler
import os
import datetime
# ## 时区为utc的问题解决：
# os.environ['TZ'] = 'Asia/Shanghai'
log = getLogger(__name__)
def beijing(sec, what):
    beijing_time = datetime.datetime.now() + datetime.timedelta(hours=8)
    return beijing_time.timetuple()


logging.Formatter.converter = beijing
###


# Use an absolute path to prevent file rotation trouble.
logfile = os.path.abspath("/home/program/sound2note/mylogfile.log")
ch = logging.StreamHandler()
#ch.setLevel(logging.INFO)

print(logfile)
# Rotate log after reaching 512K, keep 5 old copies.
rotateHandler = ConcurrentRotatingFileHandler(logfile, "a", 512*1024, 5)

#定义handler的输出格式

#formatter = logging.Formatter('%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b%Y %H:%M:%S’)

formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d]  - %(levelname)s - %(message)s',datefmt='%b%d,%H:%M:%S')
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)

rotateHandler.setFormatter(formatter)
rotateHandler.setLevel(logging.DEBUG)

log.addHandler(rotateHandler)
log.addHandler(ch)
log.setLevel(logging.DEBUG)
#log.info("Here is a very exciting log message, just for you")
##

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"
app.config['DEBUG']=True

postQueue=queue.Queue(100)

@app.route("/")
def index():
    return "Hello world"


@app.route("/query", methods=["POST","GET"])
def users():
    try:
        # data_url=request.form.get('data_url')
        jsonData = request.get_json()
        msg=jsonData['msg']

        assert len(msg)>0
        dataArray = [msg]
        log.info('backend dataArray:'+str(dataArray))
    except:
        log.warning('XXXX LACK of data_url')
        return jsonify(
            {'result_code': 'fail', "error_code": str(-2), 'error_desc': 'lack of param data_url'})
    postQueue.put(dataArray)
    # try:
    #    title,save_url= ma.saveClip(data_url)
    # except Exception as e:
    #     title=""
    #     save_url=""
    #     traceback.print_exc()

    return jsonify(
        {'result_code': "success", "error_code": '0', 'error_desc': ''})

def main(port):
    port=int(port)
    # args.port=port
    log.info('port'+str(port))
    msgQueue=Queue(100) #输入框队列
    stateQeue=Queue(maxsize=100) # 状态队列，用于处理非双工的情况（会录回系统播放的声音）
    duplex=False # True双工，False 非双工

    ## 用户语音输入框处理模块,过滤出用户最新说的那些话
    inp=moduleInput.inputClass(msgQueue,stateQeue,postQueue,duplex=duplex,logger=log)

    ##  输出模块，控制语音播放或toast输出
    ouputer=moduleOutput.outputManager(stateQeue,logger=log)

    ## 文本内容处理，这里载入了moduleNer进行理解
    processer=moduleProcesser.processerClass(logger=log)

    ## 对话管理模块，整体对话管理，唤醒词识别，输出触发
    cm=moduleConversation.converManager(msgQueue,stateQeue,strategyDict,ouputer,processer, \
     wuWordList=['小太阳','太阳'],duplex=duplex,logger=log)

    cm.daemon = True
    inp.start()
    cm.start()

#    app.run(host="0.0.0.0", port=port, debug=False)  # 启动app的调试模式
    server=WSGIServer(("0.0.0.0",port),app)
    server.serve_forever()
    cm.join()


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except:
        log.info('no args input ----------')
        main(7000)

