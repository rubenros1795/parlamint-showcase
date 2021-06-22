import re, string,os,random
from glob import glob as gb
import pandas as pd
from collections import Counter
from tqdm import tqdm
import subprocess
import nltk
from functions import *
from gensim.models import keyedvectors

def clean_subset(iso,language,start,end):
    df = data_loader.load_month(iso,start,end)
    df = df = df[df['text'].notna()]
    if language in os.listdir('/home/ruben/nltk_data/corpora/stopwords/'):
        stopwords_ = nltk.corpus.stopwords.words(language)
    else:
        stopwords_ = []
    df['text'] = [[w for w in str(t).split(' ') if "_" in w and len(w.split('_')) != 1] for t in df['posner']]
    df['text'] = [" ".join([w.split('_')[0] for w in text if w.split('_')[1] in ['NOUN','VERB','ADJ']]) for text in df['text']]
    df['text'] = [utils.preprocess(str(x),stopwords_) for x in tqdm(df['text'])]
    print("size after subsetting:",len(df))
    return df.drop(['lemmatized','title'],axis=1)


for iso,language in [('es','spanish'),('dk','danish')]:

    for subcorpus in ['covid','reference']:
        print(subcorpus)
        if subcorpus == 'reference':
            data = clean_subset(iso,language,"2019-01","2020-02")

        if subcorpus == 'covid':
            data = clean_subset(iso,language,"2020-02","2021-03")

        texts = [t.split(' ') for t in data['text']]

        print("training models with",len(texts),"speeches")
        
        model = gensim.models.Word2Vec(texts, min_count=10, workers=8)
        model.wv.save_word2vec_format(f"/home/ruben/Documents/GitHub/ParlaMintCase/results/models/{iso}-{subcorpus}.bin", binary=True)