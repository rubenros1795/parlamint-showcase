# Script for generating files with total number of words, sentences and tokens based on metadata .json file.
# Based on months as time-units.

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
import json

base_path = "/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase"


def month_generator(start_month,end_month):
    dates = [start_month, end_month]
    start, end = [datetime.strptime(_, "%Y-%m") for _ in dates]
    return list(OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m"), None) for _ in range((end - start).days)).keys())

def totals_months(months,language,unit):
    with open(f"/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/original/{language}/metadata/metadata.json",'r') as f:
        td = json.load(f)

    mt = []
    for m in months:
        mt.append([m,sum([v[unit] for k,v in td.items() if m in k])])
    
    mt = pd.DataFrame(mt,columns=['month','n'])
    mt.to_csv(os.path.join(base_path,"resources","totals",f"{language}-total-{unit}.csv"),index=False)


months = month_generator("2015-01","2020-12")

if __name__ == "__main__":
    language = sys.argv[0]
    for u in ['words','sentences','tokens']:
        totals_months(months,language,u)