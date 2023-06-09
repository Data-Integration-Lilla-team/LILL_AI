import pandas as pd
import spacy        #per la lemmizzazione delle parole
from wordcloud import WordCloud
import string
from stop_words import get_stop_words
from nltk.corpus import stopwords
import json
import glob
import re
import json
import matplotlib.pyplot as plt
import numpy as np
'''
Classe specializzata nella puliza dei dati
1. eliminazione stopwords
2. eliminazione parole con lunghezza minor di 2
3. eliminazione simboli non lettere (non presenti nella lista di punctuations di string.punctuations)
4. lemming delle parole
5. può continuare

'''

class DataCleaner:
    
    def __init__(self):
        self.index_path=r"dataExtraction\output\index_csv.csv"
        self.symbols_path=r"dataCleaning\symbols.json"
        self.puntuations=self.read_symbols(self.symbols_path)
        self.puntuations.update(["•","–"])       #da aggiungere altri custom punctuation
        self.max_length=16
        self.min_length=1


    def read_symbols(self,path):
        with open(path, 'r') as file:
            json_data = file.read()

        # Convert the JSON data back to a list
        set_list = json.loads(json_data)

        # Convert the list to a set
        my_set = set(set_list)
        return my_set


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
                if len(word)<self.max_length and len(word)>self.min_length:
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

    def remove_custom_punct(self,text):
        translator = str.maketrans('', '', ''.join(self.puntuations))
        return text.translate(translator)

    def remove_doubleCharWords(self,line):
        words=line.split()
        final=[]
        for i in words:
            if len(i)>2:
                words=self.remove_custom_punct(i)
                final.append(words)
            
                
        final=" ".join(final)

        return final
        
    def lemming_text(self, text):
        # Load the Italian language model
        nlp = spacy.load("it_core_news_sm")
        # Process the text with spaCy
        doc = nlp(text)
        # Lemmatize each token in the text
        lemmas = [token.lemma_ for token in doc]
        # Print the lemmas
        text=" ".join(lemmas)
        return text
    
            
    def find_none_spaced_words(self,text):
       
       
            
        text_with_space = re.sub(r"(\w)([A-Z])", r"\1 \2", text)

        
        return text_with_space

    def delete_double_spaces(self,text):
        text_without_double_spaces = re.sub(r"\s+", " ", text)
        return text_without_double_spaces
    

    def clean_text(self, data):
        new_text=[]
        stops=stopwords.words("italian")
        stops.extend(stopwords.words("english"))
        for i in data:

            if type(i)==type("s"):
                #rimozione di tutte le parole che non hanno lunghezza maggiore di 2
                parsed_text=self.find_none_spaced_words(i)              #andiamo a dividere eventuali parole distinte, concatenate (es. HelloWord->Hello World)
                parsed_text=self.remove_stops(parsed_text,stops)                  #rimozione stopwords
                parsed_text=self.remove_doubleCharWords(parsed_text)    #rimozione parole e simboli superflui
                parsed_text=self.delete_double_spaces(parsed_text)
                parsed_text=self.lemming_text(parsed_text)              #lemming delle parole
                
            else:
                parsed_text=""
                
            new_text.append(parsed_text)

        return new_text
    
    def clean_data(self):
        data=self.load_data()
        clean_data=self.clean_text(data["text"])
        #altri metodi di cleaning vanno inseiti qui
        data["parsed_text"]=clean_data
        data = data.sort_values(by=['path', 'page'])
        data.to_csv(r"dataCleaning\output\index_csv_parsed.csv",index=False)
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
    cleaner.clean_data()       #parsa i dati e li memorizza in una nuova colonna dell'indice csv
    #cleaner.create_word_cloud()
    
