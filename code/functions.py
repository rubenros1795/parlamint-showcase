# Script containing classes and functions for analysis

from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime, timedelta, date
from gensim.models import KeyedVectors
from scipy.cluster.vq import kmeans,vq
from collections import OrderedDict
import matplotlib.pyplot as plt
from collections import Counter
from numpy import vstack,array
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


class utils():
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
        with open(f"/home/ruben/Documents/GitHub/ParlaMintCase/data/original/{language}/metadata/metadata.json",'r',encoding='utf-8') as f:
            metadata = json.load(f)

        metadata_tags = list(set(list(metadata.items())[0][1].keys()))
        for c in metadata_tags:
            data[c] = [metadata[i][c] for i in data['id']]
        return data

    def windowizer(data,words=[],window=5):
        #"""
        #:param data: dataset with id and text columns
        #:type data: pandas DataFrame object
        #:param words: words to be considered
        #:type language: list
        #:param window: window to analyze, both left and right of keyword
        #:type window: int
        #"""
        result = []
        for c,text in enumerate(data['text']):
            text = str(text).split(' ')
            indices = [c for c,i in enumerate(text) if i in set(words)]
            for c_,ind_ in enumerate(indices):
                left = ind_- window
                right = ind_ + window
                if left < 0:
                    left = 0
                if right > len(text):
                    right = len(text)
                result.append([f"{data['id'][c]}-{c_}"," ".join(text[left:right])])
        return pd.DataFrame(result,columns=['id','window'])

    def find_date(text):
        return re.search(r'(\d+-\d+-\d+)',text).group(0)

    def preprocess_(list_txt,lowercase=True,tokenize=False,remove_punc=True,stopwords=[]):
        if lowercase == True:
                list_txt = [str(v).lower() for v in list_txt]
        if remove_punc == True:
            list_txt = [re.sub('[%s]' % re.escape(string.punctuation), '', str(v)) for v in list_txt]
        if tokenize == True:
            list_txt = [str(v).split(' ') for v in list_txt]
        list_txt = [re.sub(' +', ' ', x) for x in list_txt]
        list_txt = [" ".join([w for w in t.split(' ') if w not in set(stopwords)]) for t in list_txt]
        return list_txt 

class data_loader():

    def file(fn):
        #"""
        #:param fn: filename
        #:type fn: str
        #"""
        if os.path.exists(fn):
            return pd.read_csv(fn,sep='\t')
        else:
            print("no DataFrame found")

    def full(language,data_version="preprocessed"):
        #"""
        #:param language: language of dataset in ISO 639 format
        #:type language: str
        #:param data_version: version of the data, preprocessed, raw or lemmatized
        #:type data_version: str
        #"""
        config_options = {"preprocessed":f"{language}/{language}-txt-preproc/","lemmatized":f"{language}/{language}-ana-txt/","raw":f"{language}/{language}-txt/"}

        files_path = os.path.join(base_path + "/data/original",config_options[data_version])
        list_files = gb(files_path + "*")
        print("found",len(list_files),"files in:",files_path)
        if data_version == "raw":
            list_files = [x for x in list_files if "ParlaMint" in x and "meta" not in x]
        data = pd.DataFrame()
        for f in list_files:
            tdf = pd.read_csv(f,sep='\t')
            data = data.append(tdf)
        data.columns = ["id","text"]
        return data.reset_index(drop=True)

    def period(language="",data_version="preprocessed",start_date="",end_date=""):
        # """
        # :parameter language: language of dataset in ISO 639 format
        # :type language: str
        # :param data_version: version of the data, preprocessed, raw or lemmatized
        # :type: data_version str
        # """
        if len(start_date) == 10:
            periods = utils.day_generator(start_date,end_date)
        if len(start_date) == 7:
            format_date = "month"
            periods = utils.month_generator(start_date,end_date)

        config_options = {"preprocessed":f"{language}/{language}-txt-preproc/","lemmatized":f"{language}/{language}-ana-txt/","raw":f"{language}/{language}-txt/"}
        files_path = os.path.join(base_path + "/data/original",config_options[data_version])

        data = pd.DataFrame()
        files_period = [x for x in gb(files_path + "*") if any(p in x for p in periods) == True and "meta" not in x]
        print(files_path)
        for f in files_period:
            tdf = pd.read_csv(f,sep='\t')
            data = data.append(tdf)
        data.columns = ["id","text"]
        return data.reset_index(drop=True)

    def subset(data,words=[]):
        ss = [c for c,i in enumerate(data['text']) if any(w in set(i.split(' ')) for w in words) == True]
        data = data.iloc[ss,:].reset_index(drop=True)
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
        
        return data

    def distribution(freq_info,metadata_selectors):
        freq_info = freq_info[["date"] + metadata_selectors + [c for c in freq_info.columns if "hits" in c]]
        return freq_info.groupby(['date'] + metadata_selectors).sum().reset_index()

    def pmi_windows(text,words=[],window=5):
        list_windows = []
        text = text.split(' ')
        indices = [c for c,i in enumerate(text) if i in set(words)]
        for ind_ in indices:
            left = ind_- window
            right = ind_ + window
            if left < 0:
                left = 0
            if right > len(text):
                right = len(text)
            list_windows.append(text[left:right])
        return list_windows

    def get_pmi_table(data,date,window,word,stopwords):
        data = data[data['id'].str.contains(date)]
        data['text'] = data['text'].astype(str)

        all_words = [i.split(' ') for i in data['text']]
        all_words = Counter([item for sublist in all_words for item in sublist])
        N = sum(all_words.values())

        windows = [frequency.pmi_windows(str(x),words=[word],window=window) for x in data['text']]
        windows = [set(item) for sublist in windows for item in sublist if len(sublist) > 0]

        candidates = set([item for sublist in windows for item in sublist if item not in stopwords and len(item) > 3 and '-' not in item and all_words[item] > 5])

        d = []
        for candidate in candidates:

            p1 = all_words[word]
            p2 = all_words[candidate]
            p12 = len([x for x in windows if candidate in x and word in x])

            if p12 > 0:
                try:
                    pmi_reg = math.log(((p12) / (p1 * p2)), 2)
                    pmi_2 = math.log(((p12 ** 2) / (p1 * p2)), 2)
                    pmi_3 = math.log(((p12 ** 3) / (p1 * p2)), 2)
                    npmi = pmi_reg / - math.log(p12)
                    d.append([candidate,p1,p2,p12,pmi_reg,pmi_2,pmi_3,npmi])
                except:
                    continue

        d = pd.DataFrame(d,columns=['w','p1','p2','p12','pmi_reg','pmi_2','pmi_3','npmi'])
        return d

class cluster():
    def generate_matrix(list_words,model_name):
        model = KeyedVectors.load(model_name)
        vocab = set(list(model.wv.vocab))
        list_words = [w for w in set(list_words) if w in vocab]
        print("created list with " + str(len(list_words)) + " words")

        total_list = list()
        
        for word in list_words:
            
            list_word = list()
            
            for term in list_words:
                tmp = model.similarity(word, term)
                list_word.append(tmp)
            
            total_list.append(list_word)
        df = pd.DataFrame(total_list, columns = list_words, index = list_words)
        return df

    def cluster_word(matrix, k):
        centroids,_ = kmeans(matrix,k)
        idx,_ = vq(matrix,centroids)
        
        return dict(zip(list(matrix.index), idx))


class polarity(object):
    def __init__(self,language):
        self.pos_words_chen = set(pd.read_csv(base_path + f'/resources/lexicons/sentiment-lexicons/positive_words_{language}.txt',header=None)[0])
        self.neg_words_chen = set(pd.read_csv(base_path + f'/resources/lexicons/sentiment-lexicons/negative_words_{language}.txt',header=None)[0])

        with open(base_path + f'/resources/lexicons/sentistrength-lexicons/{language}.txt','r',encoding='utf-8') as f:
            c = f.readlines()
            self.sentistrength_data = [x.replace('\n','').split('\t') for x in c]
    
    def grouper(n, iterable, fillvalue=None):
            args = [iter(iterable)] * n
            return itertools.zip_longest(*args, fillvalue=fillvalue)

    def chen_classifier(self,text):
        text = text.split(' ')
        s =0
        for w in text:
            if w in self.pos_words_chen or w in self.neg_words_chen:
                s += 1
        return s / len(text)

    def polyglot_classifier(self,text):
        text = Text(text)
        r = sum([w.polarity for w in text.words]) / len(text.words)
        return r

    def sentistrength_classifier(self,text):
        text = text.split(' ')
        d = []
        for x in self.sentistrength_data:
            x = list(polarity.grouper(2,x))
            for i in x:
                d.append(i)
        d = [(x[0].replace(u'\xa0', u' ').replace(' ',''),x[1]) for x in d]
        d = dict(d)
        s = []
        for w in text:
            if w in set(d.keys()):
                s += int(d[w])
        return sum(s) / len(s)

class embeddings():
    def train_diachronic(data,start_date,end_date,min_count=25, workers=6, iter=10, size = 100, window = 15):
        if len(start_date) == 10:
            periods = utils.day_generator(start_date,end_date)
        if len(start_date) == 7:
            format_date = "month"
            periods = utils.month_generator(start_date,end_date)

        for count,time_ in enumerate(periods):
            if count == 0:
                texts = [data['text'][c] for c,x in enumerate(data['id']) if time_ in str(x)]
                texts = [t.split(' ') for t in texts]
                print(time_,len(texts))
                model = gensim.models.Word2Vec(texts, min_count=min_count, workers=workers, iter=iter, size = size, window = window)
                model.wv.save_word2vec_format(os.path.join(base_path + f"/results/models/{language}/{language}-{'_'.join(words_fn)}-{time_}-model.bin"), binary=True)
            if count != 0:
                texts = [data['text'][c] for c,x in enumerate(data['id']) if time_ in str(x)]
                texts = [t.split(' ') for t in texts]
                model.build_vocab(texts, update=True)
                model.train(texts, total_examples = model.corpus_count, start_alpha = model.alpha, end_alpha = model.min_alpha, epochs = model.iter)
                model.wv.save_word2vec_format(os.path.join(base_path + f"/results/models/{language}/{language}-{'_'.join(words_fn)}-{time_}-model.bin"), binary=True)
                print(time_,len(texts))

    def train(data,min_count=25, workers=6, iter=10, size = 100, window = 15):
        texts = [t.split(' ') for t in data['text']]
        words = [x.replace('_hits','') for x in data.columns if "_hits" in x]
        model = gensim.models.Word2Vec(texts, min_count=min_count, workers=workers, iter=iter, size = size, window = window)
        model.wv.save_word2vec_format(os.path.join(base_path + f"/results/models/{language}/{language}-{'_'.join(words)}-model.bin"), binary=True)
        return model

class plotting():
    def style_(pal,n_var):
        sns.set(font='Inter, Medium',rc={'axes.xmargin':0,'axes.ymargin':0,'axes.axisbelow': True,'axes.edgecolor': 'lightgrey','axes.facecolor': 'None', 'axes.grid': True,'grid.color':'whitesmoke','axes.labelcolor':'dimgrey','axes.spines.top': True,'figure.facecolor': 'white','lines.solid_capstyle': 'round','patch.edgecolor': 'w','patch.force_edgecolor': True,'text.color': 'dimgrey','xtick.bottom': True,'xtick.color': 'dimgrey','xtick.direction': 'out','xtick.top': False,'ytick.color': 'dimgrey','ytick.direction': 'out','ytick.left': False, 'ytick.right': False})
        sns.set_context("notebook", rc={"font.size":16,"axes.titlesize":20, "axes.labelsize":16})
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
        return DenseTfIdf(sublinear_tf=True, max_df=0.5,min_df=2,encoding='ascii',lowercase=True,stop_words='english',**kwargs).fit_transform(texts)

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
