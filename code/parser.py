import re, string
from glob import glob as gb
import pandas as pd

BASE_PATH = ""

class debate(object):
    """
    Class for parsing parliamentary proceedings in .txt format. 
    :date - str() - y-m-d
    """

    def __init__(self,date):
        self.date = date
        self.filename_meta = os.path.join(BASE_PATH,"data",f"ParlaMint-PL_{self.date}-sejm-01-1.meta.txt")
        self.filename = os.path.join(BASE_PATH,"data",f"ParlaMint-PL_{self.date}-sejm-01-1.txt")

    def debates(self):
        with open(self.filename,'r') as f:
            debates = f.readlines()
            debates = [x.replace('\n','').split('\t') for x in debates]
            debates = {x[0]:x[1] for x in debates}
        self.debates = debates
        return self.debates

    def metadata(self):
        with open(self.filename_meta,'r') as f:
            m = f.readlines()
            debates = [x.replace('\n','').split('\t') for x in debates]
            debates = {x[0]:x[1] for x in debates}
        self.debates = debates
        return self.debates