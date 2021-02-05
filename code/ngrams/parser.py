import re, string,os
from glob import glob as gb
import pandas as pd
from collections import Counter

class DebateParser(object):
    """
    Class for parsing parliamentary proceedings in .txt format. 
    date (str): - date to be parsed. Format is y-m-d
    """

    def __init__(self,fn):
        self.filename = fn
        self.filename_metadata = fn.replace('.txt','') + ".meta.txt" 

    def debates(self):
        with open(self.filename,'r') as f:
            self.debates = f.readlines()
        self.debates = [x.replace('\n','').split('\t') for x in self.debates]
        self.debates = {x[0]:x[1] for x in self.debates}
        return self.debates

    def metadata(self):
        self.metadata_ = pd.read_csv(self.filename_metadata,sep='\t')
        self.metadata = {}

        for c,v in enumerate(self.metadata_['ID']):
            t = {}
            for col in list(self.metadata_.columns)[1:]:
                t.update({col.lower():self.metadata_[col][c]})
            self.metadata.update({v:t})
        return self.metadata

    def preprocessed(self,lowercase=True,tokenize=True,remove_punc=True):
        debates_editable = self.debates
        if lowercase == True:
            debates_editable = {k:v.lower() for k,v in debates_editable.items()}
        if remove_punc == True:
            debates_editable = {k:re.sub('[%s]' % re.escape(string.punctuation), '', v) for k,v in debates_editable.items()}
        if tokenize == True:
            debates_editable = {k:v.split(' ') for k,v in debates_editable.items()}
        self.preprocessed = debates_editable
        return self.preprocessed


    
    