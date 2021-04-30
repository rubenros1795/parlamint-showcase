import re, string,os
from glob import glob as gb
import pandas as pd
from tqdm import tqdm
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-l', '--language', dest="language", required=True)
args = parser.parse_args()

base_path = "/home/ruben/Documents/GitHub/ParlaMintCase"
original_path = base_path + "/data/original"

def preprocess(fn,lowercase=True,tokenize=False,remove_punc=True):
    try:
        f = pd.read_csv(fn,sep='\t',header=None)
    except Exception as e:
        print(e)
        return
    # f.columns = "id text".split(' ')

    if lowercase == True:
            f[1] = [v.lower() for v in f[1]]
    if remove_punc == True:
        f[1] = [re.sub('[%s]' % re.escape(string.punctuation), '', v) for v in f[1]]
    if tokenize == True:
        f[1] = [v.split(' ') for v in f[1]]
    return f 

def preprocess_language(lan=""):
    language_original_path = os.path.join(original_path,f"{lan}/{lan}-txt")
    language_pp_path = os.path.join(original_path,f"{lan}/{lan}-txt-preproc")
    list_files = [x for x in gb(language_original_path + "/*") if "meta" not in x and "READ" not in x]
    print(f'found {len(list_files)} files for {lan}')
    if os.path.exists(language_pp_path) == False:
        os.mkdir(language_pp_path)

    for f in tqdm(list_files):
        try:
            file = preprocess(f)
            fn = os.path.join(language_pp_path,os.path.split(f)[-1])
            file.to_csv(fn,sep='\t',index=False)
        except Exception as e:
            print(e)
            continue

if __name__ == "__main__":
    language = args.language
    preprocess_language(language)