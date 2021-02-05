import re, string,os
from glob import glob as gb
import pandas as pd
from collections import Counter
from tqdm import tqdm
from datetime import datetime, timedelta, date
from collections import OrderedDict
import subprocess

class FrequencyParser(object):

    def __init__(self,words=[],months=[],exact_match=True):
        self.words = words
        self.months = months
        self.exact_match = exact_match

    def metadata(self,fn,id_):
        fn = os.path.join("/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/pl-txt",fn.replace('.txt','.meta.txt'))
        df = pd.read_csv(fn,sep='\t')
        df = df[df["ID"] == id_]
        return df

    def Parse(self):
        path = "/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/pl-txt-preproc/*"
        data = pd.DataFrame()
        for month in self.months:
            try:
                grp = "egrep -iE '" + "|".join(self.words) + "' " + path.replace('*',f'*{month}*')
                output = subprocess.check_output(grp,shell=True).decode('utf-8')
                output = [l.split('\t') for l in output.split('\n')]
                if len(output) > 0:
                    output = pd.DataFrame(output)
                    data = data.append(output)
            except Exception as e:
                continue
        
        data.columns = ["id","text"]
        data["id"] = [os.path.split(x)[-1] for x in data["id"]]
        df = pd.DataFrame(data) 
        fn = '/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/results/frequencies/'
        fn = fn + f"{'_'.join(self.words)}-{self.months[0].replace('-','_')}-{self.months[-1].replace('-','_')}.txt"

        df = df.dropna()

        for word in self.words:       

            if self.exact_match == True:
                df[f"{word}_hits"] = [dict(Counter(i.split(' ')))[word] if word in set(i.split(' ')) else 0 for i in df['text']]
            if self.exact_match == False:
                lc = []
                for t in df['text']:
                    len_ = len([w for w in t if w == word or word in w])
                df[f"{word}_hits"] = lc
        
        df.to_csv(fn,sep="\t",index=False)

        mtd_long = []
        for c,id_ in enumerate(df['id']):
            mtd = self.metadata(id_.split(':')[0],id_.split(':')[1])
            mtd = list(mtd.iloc[0,1:])
            mtd_long.append(mtd)
        mtd_long = pd.DataFrame(mtd_long,columns='term session sitting date subcorpus speaker_id speaker_name speaker_role speaker_type speaker_party speaker_party_name speaker_gender speaker_birth segments sentences names tokens words'.split(' '))

        for col in mtd_long.columns:
            df[col] = mtd_long[col]
        return df

    def month_totals(self):
        mt = []
        for m in self.months:
            list_files = [i for i in gb('/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/pl-txt/*meta*') if m in i]
            total =[]
            for f in list_files:
                total += subprocess.check_output(f"cut -f18 '{f}'",shell=True).decode('utf-8').split('\n')[1:]

            mt.append([m,sum([int(x) if x else 0 for x in total])])
        return dict(mt)


