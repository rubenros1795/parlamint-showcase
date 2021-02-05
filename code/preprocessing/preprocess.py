import re, string,os
from glob import glob as gb
import pandas as pd
from tqdm import tqdm

def preprocess(fn,lowercase=True,tokenize=False,remove_punc=True):
    f = pd.read_csv(fn,sep='\t',header=None)
    # f.columns = "id text".split(' ')

    if lowercase == True:
            f[1] = [v.lower() for v in f[1]]
    if remove_punc == True:
        f[1] = [re.sub('[%s]' % re.escape(string.punctuation), '', v) for v in f[1]]
    if tokenize == True:
        f[1] = [v.split(' ') for v in f[1]]
    return f 



for f in tqdm([x for x in gb("/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/pl-txt/*") if "meta" not in x]):
    nf = preprocess(f)
    fn = os.path.join("/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/pl-txt-preproc/",os.path.split(f)[-1])
    nf.to_csv(fn,sep='\t',index=False)
