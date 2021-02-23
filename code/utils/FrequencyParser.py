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

def MonthGenerator(start_month,end_month):
    dates = [start_month, end_month]
    start, end = [datetime.strptime(_, "%Y-%m") for _ in dates]
    return list(OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m"), None) for _ in range((end - start).days)).keys())

def preprocess(list_strings,lowercase=True,tokenize=False,remove_punc=True):
        if lowercase == True:
                list_strings = [v.lower() for v in list_strings]
        if remove_punc == True:
            list_strings = [re.sub('[%s]' % re.escape(string.punctuation), '', v) for v in list_strings]
        if tokenize == True:
            list_strings = [v.split(' ') for v in list_strings]
        return list_strings

class Parser(object):

    def __init__(self,words=[],months=[],language="",exact_match=True):
        self.words = words
        self.months = months
        self.exact_match = exact_match
        self.language = language

    def metadata(self,fn,id_):
        fn = os.path.join(f"/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/{self.language}/{self.language}-txt",fn.replace('.txt','.meta.txt'))
        df = pd.read_csv(fn,sep='\t')
        df = df[df["ID"] == id_]
        return df

    def Result(self,save_file=True):
        path = f"/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/original/{self.language}/{self.language}-txt-preproc/*"
        data = pd.DataFrame()
        for month in tqdm(self.months):
            try:
                grp = "egrep -iE '" + "|".join(self.words) + "' " + path.replace('*',f'*{month}*')
                output = subprocess.check_output(grp,shell=True).decode('utf-8')
                output = [l.split('\t') for l in output.split('\n')]
                if len(output) > 0:
                    output = pd.DataFrame(output)
                    data = data.append(output)
            except Exception as e:
                print(e)
                continue
        
        data.columns = ["id","text"]
        data["id"] = [os.path.split(x)[-1] for x in data["id"]]
        df = pd.DataFrame(data) 
        fn = f'/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/results/frequencies/{self.language}/'
        fn = fn + f"{'_'.join(self.words)}-{self.months[0].replace('-','_')}-{self.months[-1].replace('-','_')}.txt"
        df['text'] = preprocess([str(x) if x else "" for x in df['text']])
        df = df.dropna()

        for word in self.words:       

            if self.exact_match == True:
                df[f"{word}_hits"] = [dict(Counter(i.split(' ')))[word] if word in set(i.split(' ')) else 0 for i in df['text']]
            if self.exact_match == False:
                lc = []
                for t in df['text']:
                    len_ = len([w for w in t if w == word or word in w])
                df[f"{word}_hits"] = lc
        
        mtd_long = []
        for c,id_ in enumerate(df['id']):
            try:
                mtd = self.metadata(id_.split(':')[0],id_.split(':')[1])
                mtd = list(mtd.iloc[0,1:])
                mtd_long.append(mtd)
            except Exception as e:
                mtd_long.append(["","","","","","","","","","","","","","","","",""])
        mtd_long = pd.DataFrame(mtd_long,columns='term session sitting date subcorpus speaker_id speaker_name speaker_role speaker_type speaker_party speaker_party_name speaker_gender speaker_birth segments sentences names tokens words'.split(' '))

        for col in mtd_long.columns:
            df[col] = mtd_long[col]
        self.dfr = df
        if save_file == True:
            df.to_csv(fn,sep="\t",index=False)
        return df

    def month_totals(self):
        mt = []
        for m in self.months:
            list_files = [i for i in gb(f'/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/{self.language}/{self.language}-txt/*meta*') if m in i]
            total =[]
            for f in list_files:
                total += subprocess.check_output(f"cut -f18 '{f}'",shell=True).decode('utf-8').split('\n')[1:]

            mt.append([m,sum([int(x) if x else 0 for x in total])])
        self.month_totals = dict(mt)
        return dict(mt)


    def Plotter(self,party=True,dfr=None):
        if dfr != None:
            d = pd.read_csv(dfr,sep='\t')
        else:
            dfr = self.dfr

        # Plot - Set Visuals
        sns.set(font='Inter, Medium',rc={'axes.axisbelow': True,'axes.edgecolor': 'lightgrey','axes.facecolor': 'None', 'axes.grid': True,'grid.color':'lightblue','axes.labelcolor':'dimgrey','axes.spines.top': True,'figure.facecolor': 'white','lines.solid_capstyle': 'round','patch.edgecolor': 'w','patch.force_edgecolor': True,'text.color': 'dimgrey','xtick.bottom': False,'xtick.color': 'dimgrey','xtick.direction': 'out','xtick.top': False,'ytick.color': 'dimgrey','ytick.direction': 'out','ytick.left': False, 'ytick.right': False})
        sns.set_context("notebook", rc={"font.size":16,"axes.titlesize":20, "axes.labelsize":16})
        sns.set_palette("Accent",9)
        
        if party == True:
            for word in self.words:
                dfr = self.dfr[['id',f'{word}_hits','speaker_party']]
                dfr = dfr[dfr['id'] != '']
                dfr['id'] = [x.split('_')[1][:7] for x in dfr['id']]
                dfr.columns = ['month','hits','party']
                dfr['hits'] = [x / self.month_totals[list(dfr['month'])[c]] for c,x in enumerate(list(dfr['hits']))]
                dfr = dfr.groupby(['month','party']).sum().reset_index()
                dfr = dfr.pivot(index='month',columns='party',values='hits').reset_index()
                dfr.plot.bar(x='month',y=list(dfr.columns)[1:],stacked=True,figsize=(20,10))
                plt.legend(fontsize=18, bbox_to_anchor=[1, 1], loc='upper left')
                plt.xlabel('Months')
                plt.ylabel('Relative Frequency / Party')
                plt.title(f'Rel. Frequency of "{word}"',fontsize=20)
                plt.show()

        if party == False:

            pdf = []
            for m in self.months:
                tts = [m]
                for w in self.words:
                    s = dfr[(dfr['id'].str.contains(m)) & (dfr[f'{w}_hits'] > 0)][f'{w}_hits'].sum() / self.month_totals[m] * 100
                    tts.append(s)
                pdf.append(tts)

            df = pd.DataFrame(pdf)
            cols = ["m"]
            for c,i in enumerate(list(df.columns)[1:]):
                cols.append(self.words[c])
            df.columns = cols
            colors = ["salmon","teal","forestgreen","lightslategray","crimson","powderblue","lightpink"]
            df.plot.bar(x='m',y=self.words,stacked=False,color=colors,figsize=(10,6))
            plt.legend(fontsize=18, bbox_to_anchor=[1, 1], loc='upper left')
            plt.xlabel('Months')
            plt.ylabel('Relative Frequency')
