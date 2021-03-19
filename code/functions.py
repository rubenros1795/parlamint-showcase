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
import json
from gensim.models import KeyedVectors
import glob
import os
import string
import numpy
import re
import pandas as pd
import gensim
import random
from tqdm import tqdm
from gensim.models import KeyedVectors
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq
import numpy as np
import math
import re
import polyglot
from polyglot.text import Text
import io
import requests
import itertools

base_path = "/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase"


class utils():
    def month_generator(start_month,end_month):
        dates = [start_month, end_month]
        start, end = [datetime.strptime(_, "%Y-%m") for _ in dates]
        return list(OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m"), None) for _ in range((end - start).days)).keys())

    def day_generator(start_day,end_day):
        dates = [start_day, end_day]
        start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
        return list(OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m-%d"), None) for _ in range((end - start).days)).keys())

    def add_metadata(data,language):
        with open(f"/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/original/{language}/metadata/metadata.json",'r',encoding='utf-8') as f:
            metadata = json.load(f)

        metadata_tags = list(set(list(metadata.items())[0][1].keys()))
        for c in metadata_tags:
            data[c] = [metadata[i][c] for i in data['id']]
        return data

    def windowizer(data,words=[],window=5):
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

class data_loader():
    # Class for loading data
    # able to load full dataset for every language 
    # or subsets based on date/words

    def file(fn):
        if os.path.exists(fn):
            return pd.read_csv(fn,sep='\t')
        else:
            print("no DataFrame found")

    def full(language,data_version="preprocessed"):

        config_options = {"preprocessed":f"{language}/{language}-txt-preproc/","lemmatized":f"{language}/{language}-ana-txt/","raw":f"{language}/{language}-txt/"}

        files_path = os.path.join("/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/original",config_options[data_version])
        list_files = gb(files_path + "*")
        if data_version == "raw":
            list_files = [x for x in list_files if "ParlaMint" in x and "meta" not in x]
        data = pd.DataFrame()
        for f in list_files:
            tdf = pd.read_csv(f,sep='\t')
            data = data.append(tdf)
        data.columns = ["id","text"]
        return data.reset_index(drop=True)

    def period(language="",data_version="preprocessed",start_date="",end_date=""):
        if len(start_date) == 10:
            periods = utils.day_generator(start_date,end_date)
        if len(start_date) == 7:
            format_date = "month"
            periods = utils.month_generator(start_date,end_date)

        config_options = {"preprocessed":f"{language}/{language}-txt-preproc/","lemmatized":f"{language}/{language}-ana-txt/","raw":f"{language}/{language}-txt/"}
        files_path = os.path.join("/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/original",config_options[data_version])

        data = pd.DataFrame()
        files_period = [x for x in gb(files_path + "*") if any(p in x for p in periods) == True and "meta" not in x]
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

class windows():
    def inspect_file(data,word,window_size):

        d = []
        for c,x in enumerate(data['text']):
            x = x.split(' ')
            if word in x:
                indices = [c for c,i in enumerate(x) if i == word]
                for ind_ in indices:
                    left = ind_- window_size
                    right = ind_ + window_size
                    if left < 0:
                        left = 0
                    if right > len(x):
                        right = len(x)
                    d.append([data['id'][c]," ".join(x[left:ind_]),word," ".join(x[ind_+1:right])])

        html = f'<html>{pd.DataFrame(d,columns=["id","left","word","right"]).to_html()}</html>'

        with open(f'/media/ruben/Elements/PhD/results/windows/{word}-windows.html','w',encoding='utf-8') as f:
            f.write(html)
        print("written ",f'/media/ruben/Elements/PhD/results/windows/{word}-windows.html') 

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
                model.wv.save_word2vec_format(os.path.join(f"/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/results/models/{language}/{language}-{'_'.join(words_fn)}-{time_}-model.bin"), binary=True)
            if count != 0:
                texts = [data['text'][c] for c,x in enumerate(data['id']) if time_ in str(x)]
                texts = [t.split(' ') for t in texts]
                model.build_vocab(texts, update=True)
                model.train(texts, total_examples = model.corpus_count, start_alpha = model.alpha, end_alpha = model.min_alpha, epochs = model.iter)
                model.wv.save_word2vec_format(os.path.join(f"/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/results/models/{language}/{language}-{'_'.join(words_fn)}-{time_}-model.bin"), binary=True)
                print(time_,len(texts))

    def train(data,min_count=25, workers=6, iter=10, size = 100, window = 15):
        texts = [t.split(' ') for t in data['text']]
        words = [x.replace('_hits','') for x in data.columns if "_hits" in x]
        model = gensim.models.Word2Vec(texts, min_count=min_count, workers=workers, iter=iter, size = size, window = window)
        model.wv.save_word2vec_format(os.path.join(f"/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/results/models/{language}/{language}-{'_'.join(words)}-model.bin"), binary=True)
        return model

class plotting():
    def style_(pal,n_var):
        sns.set(font='Inter, Medium',rc={'axes.xmargin':0,'axes.ymargin':0,'axes.axisbelow': True,'axes.edgecolor': 'lightgrey','axes.facecolor': 'None', 'axes.grid': True,'grid.color':'whitesmoke','axes.labelcolor':'dimgrey','axes.spines.top': True,'figure.facecolor': 'white','lines.solid_capstyle': 'round','patch.edgecolor': 'w','patch.force_edgecolor': True,'text.color': 'dimgrey','xtick.bottom': True,'xtick.color': 'dimgrey','xtick.direction': 'out','xtick.top': False,'ytick.color': 'dimgrey','ytick.direction': 'out','ytick.left': False, 'ytick.right': False})
        sns.set_context("notebook", rc={"font.size":16,"axes.titlesize":20, "axes.labelsize":16})
        sns.set_palette(pal,n_var)