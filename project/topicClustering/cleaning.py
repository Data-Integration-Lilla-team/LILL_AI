import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

import string
from stop_words import get_stop_words
from nltk.corpus import stopwords
import json
import glob
import re

def load_data(file):
    with open(file, 'r',encoding="utf-8") as f:
        data=json.load(f)
    return data

def write_data(file,data):
    with open(file,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=4)

def extract_sing_pages(list_pages):
    pages_in_file=[""]
    for k in list_pages.keys():
        try:
            num_page=int(k)
            pages_in_file.insert(num_page,list_pages[k])
        except ValueError:
            pass
        
    return pages_in_file

#pipeline di pulizia
def remove_stops(text,stops):
    #rimozione data
    pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b'
    text= re.sub(pattern, '', text)
    text=text.replace("\n"," ")
    text=text.replace("-"," ")
    text=text.strip()
    text=text.lower()
    words=text.split()
    
    
    
    #rimozione stopwords
    final=[]
    for word in words:
        if word not in stops:
            final.append(word)
    final=" ".join(final)

    #punti
    final=final.translate(str.maketrans("","",string.punctuation))
    #rimozione numeri
    final="".join([i for i in final if not i.isdigit()])

    #eliminazione doppi " "
    while "  " in final:
        final=final.replace("  "," ")
    
    return (final)

 
def clean_docs(data):
    stops=stopwords.words("italian")
    final={}
    for key in data.keys():
        all_pages=data[key]
        all_pages_parsed=[""]
        for pages in all_pages:
            clean_doc=remove_stops(pages,stops)
            print("clean doc",clean_doc)
            all_pages_parsed.append(clean_doc)
            
        final[key]=all_pages_parsed
    write_data("index_parsed.json",final) 
        


def extract_data(data):
    all_pages={}
    for k in data.keys():
        name_pdf=k
        sing_pages=extract_sing_pages(data[k])
        all_pages[name_pdf]=sing_pages
    return all_pages

data=load_data("index.json")
data=extract_data(data)
clean_docs(data)
