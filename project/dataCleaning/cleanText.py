import pandas as pd

from wordcloud import WordCloud
import string
from stop_words import get_stop_words
from nltk.corpus import stopwords
import json
import glob
import re
import matplotlib.pyplot as plt


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
        data = data.sort_values(by=['path', 'page'])
        data.to_csv("index_csv_parsed.csv",index=False)
        return data["parsed_text"]


    #Mostra il word to cloud
    def create_word_cloud(self):
        data=pd.read_csv("index_csv_parsed.csv")
        data=data["parsed_text"]
        # Join the different processed titles together.
        long_string = ','.join(list(data))
        print(long_string)
        # Create a WordCloud object
        wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
        # Generate a word cloud
        wordcloud.generate(long_string)
        # Visualize the word cloud
        # Display the word cloud using matplotlib
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()



if __name__=="__main__":
    cleaner=DataCleaner()
    #cleaner.clean_data()       #parsa i dati e li memorizza in una nuova colonna dell'indice csv
    cleaner.create_word_cloud()
    
