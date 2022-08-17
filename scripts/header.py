# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 17:24:25 2022

@author: kevin
"""

class appHeaderClass():
    def __init__(self,
    app_id="cli_a17e4xxxxxxx",app_secret="sCfxxxxxxxx"):
        self.app_id = app_id
        self.app_secret = app_secret
appHeader=appHeaderClass()
docDict={"doc1":"doccn869Sw1xxxxxxxxxxxxx"}#修改回你自己的
baseDict={"base1":"bascnjkQ3EIPk7xxxxxxxxxx"}#修改回你自己的
tableDict={"base1total":"tbl72Yxxxxxxxxxxx"}#修改回你自己的
queryUrl=r"http://127.0.0.1:7000/query"
nerUrl="云函数路径"#修改回你自己的