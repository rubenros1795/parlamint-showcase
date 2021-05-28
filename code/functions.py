# Script containing classes and functions for analysis

from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime, timedelta, date
from gensim.models import KeyedVectors
from scipy.cluster.vq import kmeans,vq
from collections import OrderedDict
import matplotlib.pyplot as plt
from collections import Counter
from numpy import vstack,array
from nltk.corpus import stopwords
from polyglot.text import Text
from numpy.random import rand
from glob import glob as gb
import re, string,os,io
from tqdm import tqdm
import seaborn as sns
import pandas as pd
import numpy as np
import subprocess
import itertools
import requests
import polyglot
import string
import json
import numpy
import gensim
import random
import math


base_path = "/home/ruben/Documents/GitHub/ParlaMintCase"
data_path = "/media/ruben/Elements/ParlaMint"

class utils():
    def date_generator(format,start,end):
        if format == 'month':
            dates = [start, end]
            start, end = [datetime.strptime(_, "%Y-%m") for _ in dates]
            return list(OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m"), None) for _ in range((end - start).days)).keys())

        if format == 'week':
            if start.split('-')[0] != end.split('-')[0]:
                weeks = [f"{start.split('-')[0]}-{n}" for n in range(int(start.split('-')[1]),53)] 
                weeks += [f"{end.split('-')[0]}-{n}" for n in range(0,int(end.split('-')[1])+1)]
            else:
                weeks = [f"{start.split('-')[0]}-{n}" for n in range(int(start.split('-')[1]),int(end.split('-')[1]) + 1)] 
            return [x.replace('-','-0') if len(x) == 6 else x for x in weeks]

        if format == 'day':
            dates = [start, end]
            start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
            return list(OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m-%d"), None) for _ in range((end - start).days)).keys())
            
    def month_generator(start_month,end_month):
        #"""
        #:param start_month: first month of series
        #:type start_month: str
        #:param start_month: last month of series
        #:type start_month: str
        #"""
        dates = [start_month, end_month]
        start, end = [datetime.strptime(_, "%Y-%m") for _ in dates]
        return list(OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m"), None) for _ in range((end - start).days)).keys())

    def day_generator(start_day,end_day):
        #"""
        #:param start_month: first day of series
        #:type start_month: str
        #:param start_month: last day of series
        #:type start_month: str
        #"""
        dates = [start_day, end_day]
        start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
        return list(OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m-%d"), None) for _ in range((end - start).days)).keys())

    def add_metadata(data,language):
        #"""
        #:param data: dataset with id and text columns
        #:type data: pandas DataFrame object
        #:param language: language of dataset in ISO 639 format
        #:type language: str
        #"""
        with open(f"{data_path}/{language}/metadata/metadata.json",'r',encoding='utf-8') as f:
            metadata = json.load(f)

        metadata_tags = list(set(list(metadata.items())[0][1].keys()))
        keys_ = set(metadata.keys())

        for c in metadata_tags:
            data[c] = [metadata[i][c] for i in data['id']]
        return data

    def windowizer(data,words=[],window=5,id_column="",text_column=""):
        #"""
        #:param data: dataset with id and text columns
        #:type data: pandas DataFrame object
        #:param words: words to be considered
        #:type language: list
        #:param window: window to analyze, both left and right of keyword
        #:type window: int
        #"""
        
        result = []
        data = data.reset_index(drop=True)
        for c,text in enumerate(data[text_column]):
            text = str(text).split(' ')
            indices = [c for c,i in enumerate(text) if i in set(words)]
            for c_,ind_ in enumerate(indices):
                left = ind_- window
                right = ind_ + window
                if left < 0:
                    left = 0
                if right > len(text):
                    right = len(text)
                result.append([f"{data[id_column][c]}-{c_}"," ".join(text[left:right])])
        return pd.DataFrame(result,columns=['id','window'])

    def find_date(text):
        return re.search(r'(\d+-\d+-\d+)',text).group(0)

    def preprocess(txt,stopwords_=[]):
        translator = str.maketrans('', '', string.punctuation)
        txt = txt.translate(translator)
        txt = txt.replace('—',' ')
        txt = re.sub('\s+', ' ', txt).strip()
        txt = txt.lower()
        txt = [w for w in txt.split(' ') if w not in stopwords_ and any(c.isdigit() for c in w) == False]
        return " ".join(txt)

class data_loader():

    def load_month(language,start_month,end_month):
        months = utils.month_generator(start_month=start_month,end_month=end_month)
        files_month = [i for i in gb(f'/media/ruben/Elements/ParlaMint/data_transformed/{language}/*') if any(n in i for n in months) == True]
        li = []
        for f in files_month:
            try:
                tdf = pd.read_csv(f)
                li.append(tdf)
            except Exception as e:
                print(f,e)
                continue
        data = pd.concat(li,axis=0).reset_index(drop=True)
        data.columns = [x.lower() for x in data.columns]
        data = data.drop(['session','meeting','sitting','agenda','speaker_birth'],axis=1)
        return data
    
class frequency():
    def information(data,words,exact_match,period_format="month"):
        
        for word in words:
            if exact_match == True:
                    data[f"{word}_hits"] = [dict(Counter(str(i).split(' ')))[word] if word in set(str(i).split(' ')) else 0 for i in data['text']]
            if exact_match == False:
                lc = []
                for t in data['text']:
                    len_ = len([w for w in str(t).split(' ') if w == word or word in w])
                data[f"{word}_hits"] = lc

        if period_format == "month":
            data['date'] = [re.search(r'\d{4}-\d{2}', text).group() for text in data['id']]
        if period_format == "day":
            data['date'] = [re.search(r'\d{4}-\d{2}-\d{2}', text).group() for text in data['id']]
        if period_format == "week":
            data['date'] = [re.search(r'\d{4}-\d{2}-\d{2}', text).group() for text in data['id']]
            data['date'] = pd.to_datetime(data['date'], infer_datetime_format=True)  
            data['week'] = [str(x.isocalendar()[1]) for x in data['date']]
        return data

    def distribution(freq_info,metadata_selectors):
        freq_info = freq_info[["date"] + metadata_selectors + [c for c in freq_info.columns if "hits" in c]]
        return freq_info.groupby(['date'] + metadata_selectors).sum().reset_index()


class plotting():
    def style_(pal="Paired",n_var=12):
        sns.set(font='Inter, Medium',rc={'axes.xmargin':0,'axes.ymargin':0,'axes.axisbelow': True,'axes.edgecolor': 'lightgrey','axes.facecolor': 'None', 'axes.grid': True,'grid.color':'whitesmoke','axes.labelcolor':'black','axes.spines.top': True,'figure.facecolor': 'white','lines.solid_capstyle': 'round','patch.edgecolor': 'w','patch.force_edgecolor': True,'text.color': 'black','xtick.bottom': True,'xtick.color': 'black','xtick.direction': 'out','xtick.top': False,'ytick.color': 'black','ytick.direction': 'out','ytick.left': False, 'ytick.right': False})
        sns.set_context("notebook", rc={"font.size":16,"axes.titlesize":16, "axes.labelsize":14})
        sns.set_palette(pal,n_var)

class DenseTfIdf(TfidfVectorizer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def transform(self, x, y=None) -> pd.DataFrame:
        res = super().transform(x)
        df = pd.DataFrame(res.toarray(), columns=self.get_feature_names())
        return df

    def fit_transform(self, x, y=None) -> pd.DataFrame:
        res = super().fit_transform(x, y=y)
        #df = pd.DataFrame(res.toarray(), columns=self.get_feature_names(), index=x.index())
        return self,res

class tfidf():

    def get_docterms(data,text_column,**kwargs):
        texts = list(data[text_column])
        return DenseTfIdf(lowercase=True,**kwargs).fit_transform(texts)

    def get_topterms(tfidf_object,docterms,data,category_column):
        docterms = pd.DataFrame(docterms.toarray(), columns=tfidf_object.get_feature_names(),index=data.index)
        d = pd.DataFrame()

        for cat in set(data[category_column]):
            # Need to keep alignment of indexes between the original dataframe and the resulted documents-terms dataframe
            df_class = data[(data[category_column] == cat)]
            df_docs_terms_class = docterms.iloc[df_class.index]
            # sum by columns and get the top n keywords
            dfop = df_docs_terms_class.sum(axis=0).nlargest(n=50)
            dfop = pd.DataFrame(dfop).reset_index()
            dfop.columns = [cat + " terms",cat + " score"]
            dfop[cat + " score"] = [round(x,2) for x in dfop[cat + " score"]]

            d[cat] = dfop[cat + " terms"]
        return d
