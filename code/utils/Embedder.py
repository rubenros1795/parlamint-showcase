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
from gensim.models import Word2Vec
import nltk
from nltk.tokenize import sent_tokenize
import numpy as np
import re
import gensim
from gensim.models import KeyedVectors

def MonthGenerator(start_month,end_month):
    dates = [start_month, end_month]
    start, end = [datetime.strptime(_, "%Y-%m") for _ in dates]
    return list(OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m"), None) for _ in range((end - start).days)).keys())

def preprocess(list_strings,lowercase=True,tokenize=False,remove_punc=True):
    if lowercase == True:
            list_strings = [str(v).lower() for v in list_strings]
    if remove_punc == True:
        list_strings = [re.sub('[%s]' % re.escape(string.punctuation), '', str(v)) for v in list_strings]
    if tokenize == True:
        list_strings = [str(v).split(' ') for v in list_strings]
    return list_strings


# def binder(text,list_pairs):
#     i = text.split(' ')
    
#     skips = []
#     newtext = []
#     for c,w in enumerate(i):
#         if c+1 <len(i):
#             if w in ["present","immediate","current"] and i[c+1] == "crisis" and c not in skips:
#                 skips.append(c+1)
#                 word = w + "_" + "crisis"
#                 newtext.append(word)
#             else:
#                 if c not in skips:
#                     newtext.append(w)
#         else:
#                 if c not in skips:
#                     newtext.append(w)
#     return " ".join(newtext)

def TrainEmbeddingsDiachronic(df,start_month,end_month,min_count=25, workers=6, iter=10, size = 100, window = 15):
    df['text'] = preprocess(list(df['text']))
    df = df.reset_index(drop=True)
    words_fn = [x.replace('_hits','') for x in df.columns if "_hits" in x]
    language = list(df['id'])[0][10:12].lower()
    months = MonthGenerator(start_month=start_month,end_month=end_month)
    month_freqs = {m:len([df['text'][c] for c,x in enumerate(df['id']) if m in str(x)]) for m in months}
    months = [m for m in months if month_freqs[m] != 0]


    print("training models with texts: ",words_fn)
    print(months)

    for count,time_ in enumerate(months):
        if count == 0:
            texts = [df['text'][c] for c,x in enumerate(df['id']) if time_ in str(x)]
            texts = [t.split(' ') for t in texts]
            print(time_,len(texts))
            model = gensim.models.Word2Vec(texts, min_count=min_count, workers=workers, iter=iter, size = size, window = window)
            model.wv.save_word2vec_format(os.path.join(f"/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/results/models/{language}/{language}-{'_'.join(words_fn)}-{time_}-model.bin"), binary=True)
        if count != 0:
            texts = [df['text'][c] for c,x in enumerate(df['id']) if time_ in str(x)]
            texts = [t.split(' ') for t in texts]
            model.build_vocab(texts, update=True)
            model.train(texts, total_examples = model.corpus_count, start_alpha = model.alpha, end_alpha = model.min_alpha, epochs = model.iter)
            model.wv.save_word2vec_format(os.path.join(f"/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/results/models/{language}/{language}-{'_'.join(words_fn)}-{time_}-model.bin"), binary=True)
            print(time_,len(texts))

def DataFrameMostSimilar(language,search_term,words,topn=15):
    d = pd.DataFrame()
    print("searching in",f'/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/results/models/{language}/*{"_".join(words)}*')
    for i in sorted(gb(f'/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/results/models/{language}/*{"_".join(words)}*')):
        m = KeyedVectors.load_word2vec_format(i,binary=True)
        try:
            d[i[-17:-10]] = list([x[0] for x in m.wv.most_similar(search_term,topn=topn)])
        except Exception as e:
            continue

    return d

def DiachronicSimilarity(language,word1,word2,words,topn=15):
    d = []
    print("searching in",f'/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/results/models/{language}/*{"_".join(words)}*')
    
    
    for i in sorted(gb(f'/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/results/models/{language}/*{"_".join(words)}*')):
        m = KeyedVectors.load_word2vec_format(i,binary=True)
        try:
            d.append([i[-17:-10],m.wv.similarity(word1,word2)])
        except Exception as e:
            continue

    return pd.DataFrame(d,columns="month similarity".split())

def TrainEmbeddingsSingle(df,min_count=25, workers=6, iter=10, size = 100, window = 15):
    df['text'] = preprocess(list(df['text']))
    df = df.reset_index(drop=True)
    texts = [t.split(' ') for t in df['text']]
    words = [x.replace('_hits','') for x in df.columns if "_hits" in x]
    language = list(df['id'])[0][10:12].lower()
    print(language,words)
    print("training on: ",len(texts),"txts")


    model = gensim.models.Word2Vec(texts, min_count=min_count, workers=workers, iter=iter, size = size, window = window)
    model.wv.save_word2vec_format(os.path.join(f"/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/results/models/{language}/{language}-{'_'.join(words)}-model.bin"), binary=True)
    return model