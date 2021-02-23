import enum
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

    def __init__(self,term1="",term2="",language="",months=[]):
        self.term1 = term1
        self.term2 = term2
        self.months = months
        self.language = language

    def month_totals(self):
        mt = []
        for m in self.months:
            list_files = [i for i in gb(f'/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/original/{self.language}/{self.language}-txt/*meta*') if m in i]
            total =[]
            for f in list_files:
                total += subprocess.check_output(f"cut -f18 '{f}'",shell=True).decode('utf-8').split('\n')[1:]

            mt.append([m,sum([int(x) if x else 0 for x in total])])
        self.month_totals = dict(mt)
        return self.month_totals

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
        return data
        
    
 
    def pmi_month(self,month):
        df1 = self.parse_term(self.term1)
        df1 = df1[df1['month'] == month]
        df2 = self.parse_term(self.term2)
        df2 = df2[df2['month'] == month]

        p1 = len(list(df1['id']))
        p2 = len(list(df2['id']))
        p12 = len(set(df1['id']).intersection(set(df2['id'])))


        if p1 == 0 or p2 == 0 or p12 == 0:
            print(0,p1,p2,p12)
            return 0

       
        pmi_ = math.log((p12) / (p1 * p2))
        print(pmi_,p1,p2,p12)
        return pmi_


months = ["2020-01","2020-02","2020-03","2020-04","2020-04","2020-05","2020-06","2020-07","2020-08"]
parser = pmi(term1="koronawirus",term2="ministrze",language='pl',months=months)

for m in months:
    parser.pmi_month(m)