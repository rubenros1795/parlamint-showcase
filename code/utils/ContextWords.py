import re, string,os
from glob import glob as gb
import pandas as pd
from collections import Counter
from tqdm import tqdm
from datetime import datetime, timedelta, date
from collections import OrderedDict
import subprocess
import matplotlib.pyplot as plt
import seaborn as sns
import math


class pmi(object):

    def __init__(self,term1="",language="",months=[]):
        self.term = term1
        self.months = months
        self.language = language
    
    def parse_term(self,term):
        path = f"/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/covid-subsets/{self.language}-covid-subset.txt"
        grp = "egrep -iE '" + term + "' " + path
        output = subprocess.check_output(grp,shell=True).decode('utf-8')
        output = [l.split('\t') for l in output.split('\n')]
        data = pd.DataFrame(output)
        data.columns = ["id","text"]
        data["id"] = [os.path.split(x)[-1] for x in data["id"]]
        data = data[data['id'].str.contains('ParlaMint')].reset_index(drop=True)
        data['month'] = [x.split('_')[1][:7] for x in data['id']]
        print(term,len(data))
        return data

    def context_words = 