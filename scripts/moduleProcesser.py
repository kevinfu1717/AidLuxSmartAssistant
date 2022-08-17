import moduleNer
class processerClass():
    def __init__(self,logger=None):
        self.logger=logger
        self.nerer=moduleNer.NerClass(method='online',logger=self.logger)
    def run(self,text):
        resultDict={}
        resultDict.update(self.nerer.run(text))
        return resultDict
