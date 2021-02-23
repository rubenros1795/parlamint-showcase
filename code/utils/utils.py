import os
import pandas as pd 

def load_freq_df(fn):
    if os.path.exists(fn):
        return pd.read_csv(fn,sep='\t')
    else:
        print("no DataFrame found, perhaps the file has another start month?")