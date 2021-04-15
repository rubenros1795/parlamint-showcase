# Script for generating .xml files containing information about government coalitions. Based on Wikipedia data and far from complete. Needs manual checking after running!!

import re, string,os
from glob import glob as gb
import pandas as pd
from tqdm import tqdm
from collections import Counter
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib
import wikipedia
from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
import xml.etree.cElementTree as ET
from dateutil.parser import parse
from fuzzywuzzy import process
from functions import *


base_path = "/home/ruben/Documents/GitHub/ParlaMintCase"

wiki_links = {"bg":["Second_Borisov_Government","Gerdzhikov_Government","Third_Borisov_Government"],
              "pl":["Cabinet_of_Beata_Szydło","First_Cabinet_of_Mateusz_Morawiecki","Second_Cabinet_of_Mateusz_Morawiecki"],
              "sl":["12th_Government_of_Slovenia","13th_Government_of_Slovenia","14th_Government_of_Slovenia"],
              "cz":["Bohuslav_Sobotka%27s_Cabinet","Andrej_Babiš%27_First_Cabinet","Andrej_Babiš%27_Second_Cabinet"],
              "en":["Second_May_ministry","First_Johnson_ministry","Second_Johnson_ministry"],
              "nl":["First_Rutte_cabinet","Second_Rutte_cabinet","Third_Rutte_cabinet"],
              "is":["Cabinet_of_Bjarni_Benediktsson_(2017)","Cabinet_of_Katrín_Jakobsdóttir"],
              "lt":["Skvernelis_Cabinet","Šimonytė_Cabinet"],
              "it":["Gentiloni_Cabinet","Conte_I_Cabinet","Conte_II_Cabinet","Draghi_Cabinet"],
              "tr":["Yıldırım_Cabinet","Cabinet_Erdoğan_IV"],
              "da":["Lars_Løkke_Rasmussen_III_Cabinet","Frederiksen_Cabinet"],
              "hu":["Second_Orbán_Government","Third_Orbán_Government","Fourth_Orbán_Government"],
              "fr":["First_Philippe_government","Second_Philippe_government","Castex_government"],
              "lv":["Second_Straujuma_cabinet","Kučinskis_cabinet","Kariņš_cabinet"],
              "ro":["Dăncilă_Cabinet","First_Orban_Cabinet","Second_Orban_Cabinet","Cîțu_Cabinet"],
              "be":["Michel_I_Government","Michel_II_Government","Wilmès_I_Government","Wilmès_II_Government","De_Croo_Government"]}


def parse_url(url):
    c = requests.get(url)
    return bs(c.content)

def find_party_name(short_url,language):
    url = 'https://en.wikipedia.org/'+ short_url
    s = parse_url(url)
    wikidata_link = [x for x in s.find_all('a') if x.text == "Wikidata item"][0].attrs['href']
    wikidata_soup = parse_url(wikidata_link)
    try:
        party_page = [x for x in wikidata_soup.find_all('span') if x.text == f"{language}wiki"][0].findParent().findParent().find('a').attrs['href']
        return parse_url(party_page).find("h1",{"id":"firstHeading"}).text
    except Exception as e:
        try:
            return wikidata_soup.find('li',{"class":"wikibase-entitytermsview-aliases-alias"}).text
        except:
            return "na"

def wikiparser(language,urls):

    # data = data_loader.full(language)
    # data = utils.add_metadata(data,language)
    # p = list(zip(data['speaker_party'],data['speaker_party_name']))
    # up = []
    # for x in p:
    #     name = x[0].split(';')
    #     abv = x[1].split(';')
    #     if len(name) > 1:
    #         for c,n in enumerate(name):
    #             up.append([n,abv[c]])
    #     else:
    #         up.append([name[0],abv[0]])

    # up = pd.DataFrame(up,columns=["abv","name"]).groupby(["abv","name"]).sum().reset_index()

    root = ET.Element("relations")

    for url in urls:
        url = 'https://en.wikipedia.org/wiki/'+url
        s = parse_url(url)
        date_formed = [x for x in s.find_all('th') if x.text == "Date formed"][0].findParent().find('td').text
        date_formed = re.sub("[\(\[].*?[\)\]]", "", date_formed)
        date_formed = parse(date_formed)
        date_formed = date_formed.strftime('%Y-%m-%d')
        try:
            date_dissolved = [x for x in s.find_all('th') if x.text == "Date dissolved"][0].findParent().find('td').text
            date_dissolved = re.sub("[\(\[].*?[\)\]]", "", date_dissolved)
            date_dissolved = parse(date_dissolved)
            date_dissolved = date_dissolved.strftime('%Y-%m-%d')
        except:
            date_dissolved = "present"

        # Member parties
        try:
            member_parties = [x for x in s.find_all('th') if x.text == "Member party"]
            if len(member_parties) == 0:
                member_parties = [x for x in s.find_all('th') if x.text == "Member parties"]
            
            member_parties = member_parties[0].findParent().find('td').find_all('a')
            names = [find_party_name(x.attrs['href'],language) for x in member_parties]
            member_parties = names#[x.text for x in member_parties]
        except Exception as e:
            member_parties = []

        # Opposition Parties
        try:
            opp_parties = [x for x in s.find_all('th') if x.text == "Opposition party"]
            if len(opp_parties) == 0:
                opp_parties = [x for x in s.find_all('th') if x.text == "Opposition parties"]
            
            opp_parties = opp_parties[0].findParent().find('td').find_all('a')
            names = [find_party_name(x.attrs['href'],language) for x in opp_parties]
            opp_parties = names#[x.text for x in member_parties]
        except Exception as e:
            opp_parties = []

        w = {"start":date_formed,"end":date_dissolved,"member_parties":member_parties,"opposition_parties":opp_parties}

        # write xml
        period = ET.Element('relation')
        period.set("name","coalition")
        period.set("mutual"," ".join([f"party.{x}" for x in w['member_parties']]))
        period.set("from",w["start"])
        period.set("to",w["end"])
        period.set("gov_name",s.find('h1').text)
        root.append(period)

        period = ET.Element('relation')
        period.set("name","opposition")
        period.set("mutual"," ".join([f"#party.{x}" for x in w['opposition_parties']]))
        period.set("from",w["start"])
        period.set("to",w["end"])
        period.set("gov_name",s.find('h1').text)

        root.append(period)
    tree = ET.ElementTree(root)
    tree.write(f"/home/ruben/Documents/GitHub/ParlaMintCase/resources/coalitions/{language}.xml",encoding="UTF-8")


for k,v in wiki_links.items():
    wikiparser(k,v)