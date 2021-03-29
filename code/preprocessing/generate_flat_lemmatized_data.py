import re, string,os
from glob import glob as gb
import pandas as pd
from collections import Counter
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import concurrent.futures
from lxml import etree
import sys

############
def rt(fn):
    with open(fn,'r') as f:
        c = f.read()
    return bs(c)

###########
def parse(fn):
    tree = etree.parse(fn)
    root = tree.getroot()
    namespaces = {}
    for k,v in root.nsmap.items():
        if not k:
            namespaces['ns'] = v

    d = {}
    for speech in root.findall('.//ns:u', namespaces):
        
        id_ = speech.attrib['{http://www.w3.org/XML/1998/namespace}id']
        speech_text = []
        for sentence in speech.findall('.//ns:s', namespaces):
            sentence_text = []
            for word in sentence.findall('.//ns:w', namespaces):
                
                lemma = word.attrib['lemma']
                sentence_text.append(lemma)
            speech_text.append(" ".join(sentence_text))
        d.update({id_:". ".join(speech_text)})
    d = pd.DataFrame(list(d.items()))
    ofn = fn.replace('-ana-xml','-ana-txt').replace('.xml','.txt')
    d.to_csv(ofn,sep='\t',index=False)

##########

if __name__ == "__main__":
    lan = sys.argv[0]
    list_ = gb(f'/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/original/{lan}/{lan}-ana-xml/*ana.xml*')
    if os.path.exists(f'/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/original/{lan}/{lan}-ana-txt/') == False:
        os.mkdir(f'/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/ParlaMintCase/data/original/{lan}/{lan}-ana-txt/')
    print("transforming items:",len(list_))
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as e:
        for u in list_:
            e.submit(parse, u)