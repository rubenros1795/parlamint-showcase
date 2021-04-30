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
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-l', '--language', dest="language", required=True)
parser.add_argument('-start','--start',dest='start',required=True)
parser.add_argument('-end','--end',dest='end',required=True)
args = parser.parse_args()


base_path = "/media/ruben/Elements/ParlaMint"


def month_generator(start_month,end_month):
    dates = [start_month, end_month]
    start, end = [datetime.strptime(_, "%Y-%m") for _ in dates]
    return list(OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m"), None) for _ in range((end - start).days)).keys())

def totals_months(months,language):

    mt = []
    for m in months:
        try:
            grp = f"cut -f2 {base_path}/{language}/{language}-txt/*{m}*"
            op = subprocess.check_output(grp,shell=True).decode('utf-8')
            len_tokens = len([x for x in re.sub('[%s]' % re.escape(string.punctuation), '', op.replace('\n',' ')).split(' ') if x != ''])
            mt.append([m,len_tokens])
        except Exception as e:
            print(e)
            mt.append([m,0])
    mt = pd.DataFrame(mt,columns=['month','n'])
    mt.to_csv(os.path.join("/home/ruben/Documents/GitHub/ParlaMintCase","resources","totals",f"{language}-total-tokens.csv"),index=False)


months = month_generator(args.start,args.end)

if __name__ == "__main__":
    language = args.language
    totals_months(months,language,)
