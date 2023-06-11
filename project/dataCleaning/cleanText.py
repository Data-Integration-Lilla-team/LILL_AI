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


class DataCleaner:
    
    def __init__(self):
        self.index_path="index_csv.csv"



    def load_data(self):
        data=pd.read_csv(self.index_path)
        return data

    def write_data(self,file,data):
        with open(file,"w",encoding="utf-8") as f:
            json.dump(data,f,indent=4)

    def extract_sing_pages(self,list_pages):
        pages_in_file=[""]
        for k in list_pages.keys():
            try:
                num_page=int(k)
                pages_in_file.insert(num_page,list_pages[k])
            except ValueError:
                pass
            
        return pages_in_file

    #pipeline di pulizia
    def remove_stops(self,text,stops):
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

    
    def clean_docs(self,data):
        stops=stopwords.words("italian")
        final={}
        for key in data.keys():
            all_pages=data[key]
            all_pages_parsed=[""]
            for pages in all_pages:
                clean_doc=self.remove_stops(pages,stops)
                print("clean doc",clean_doc)
                all_pages_parsed.append(clean_doc)
                
            final[key]=all_pages_parsed
        self.write_data("index_parsed.json",final) 
            


    def clean_text(self, data):
        new_text=[]
        stops=stopwords.words("italian")
        for i in data:
            parsed_text=self.remove_stops(i,stops)
            new_text.append(parsed_text)
        return new_text
    
    def clean_data(self):
        data=self.load_data()
        clean_data=self.clean_text(data["text"])
        #altri metodi di cleaning vanno inseiti qui
        data["parsed_text"]=clean_data

        data.to_csv("index_csv_parsed.csv",index=False)





if __name__=="__main__":
    cleaner=DataCleaner()
    cleaner.clean_data()
