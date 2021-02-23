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

def preprocess(list_strings,lowercase=True,tokenize=False,remove_punc=True):
        if lowercase == True:
                list_strings = [v.lower() for v in list_strings]
        if remove_punc == True:
            list_strings = [re.sub('[%s]' % re.escape(string.punctuation), '', v) for v in list_strings]
        if tokenize == True:
            list_strings = [v.split(' ') for v in list_strings]
        return list_strings

def Generate(fn,word):
    df = pd.read_csv(fn,sep='\t')
    sy = fn.split('-')[1][:4]
    ey = fn.split('-')[2][:4]
    df['text'] = preprocess(list(df['text']))

    d = []
    for c,x in enumerate(df['text']):
        x = x.split(' ')
        if word in x:
            indices = [c for c,i in enumerate(x) if i == word]
            for ind_ in indices:
                left = ind_- 15
                right = ind_ + 15
                if left < 0:
                    left = 0
                if right > len(x):
                    right = len(x)
                title = "S| " + df['scene_title'][c].lower()
                if title == "S| na":
                    title = "T| " + df['topic_title'][c].lower()
                d.append([df['id'][c].split(':')[-1][:10],title," ".join(x[left:ind_]),word," ".join(x[ind_+1:right])])

    html = """
    <html>

    <link rel="stylesheet" href="style.css">

    """

    html += f'{pd.DataFrame(d,columns=["id","scene_title","left","word","right"]).to_html()}</html>'

    with open(f'/media/ruben/Elements/PhD/results/windows/{word}-windows.html','w',encoding='utf-8') as f:
        f.write(html)
    
    print("written ",f'/media/ruben/Elements/PhD/results/windows/{word}-windows.html') 