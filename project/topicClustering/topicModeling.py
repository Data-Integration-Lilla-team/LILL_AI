import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import gensim
from gensim.utils import simple_preprocess
import gensim.corpora as corpora
import pandas as pd
import pyLDAvis.gensim
import pickle 
import pyLDAvis
import os
import pickle
class LDAModel:
        def __init__(self):
             
            self.stop_words = stopwords.words('italian')
            self.path_data_file="index_csv_parsed.csv"
            self.column_data="parsed_text"
            self.lda_model=None
            self.model_path=r"topicClustering\model.lda"
            self.id2word_path=r"topicClustering\id2token.mm"
            self.corpus_path=r"topicClustering\corpus.mm"
            #iperparametri
            self.number_topics=10
            self.top_k_topics=5
        
        def sent_to_words(self,sentences):
            for sentence in sentences:
                # deacc=True removes punctuations
                yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))
        def remove_stopwords(self,texts):
            return [[word for word in simple_preprocess(str(doc)) 
                    if word not in self.stop_words] for doc in texts]
        
        def load_data(self):
             return pd.read_csv(self.path_data_file)
        

        def save_model(self, model):
            with open(self.model_path,"wb") as file:
                 pickle.dump(model,file)

        #da modificare
        def view_data(self,num_topics,corpus,id2word,lda_model):
             # Visualize the topics
                pyLDAvis.enable_notebook()
                LDAvis_data_filepath = os.path.join('project\topicClustering\lda_vis_#'+str(num_topics))
                # # this is a bit time consuming - make the if statement True
                # # if you want to execute visualization prep yourself
                if 1 == 1:
                    LDAvis_prepared = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
                    with open(LDAvis_data_filepath, 'wb') as f:
                        pickle.dump(LDAvis_prepared, f)
                # load the pre-prepared pyLDAvis data from disk
                with open(LDAvis_data_filepath, 'rb') as f:
                    LDAvis_prepared = pickle.load(f)
                pyLDAvis.save_html(LDAvis_prepared, 'project\topicClustering\lda_vis_#'+ str(num_topics) +'.html')
                LDAvis_prepared


        def prepare_data(self):
             
            data = self.load_data()
            text_parsed=data[self.column_data].values.tolist()
            data_words = list(self.sent_to_words(text_parsed))
            # Create Dictionary
            id2word = corpora.Dictionary(data_words)

            #memorizzo
            id2word.save(self.id2word_path)

            
            # Create Corpus
            texts = data_words
            # Term Document Frequency
            corpus = [id2word.doc2bow(text) for text in texts]
            corpora.MmCorpus.serialize(self.corpus_path, corpus)
            # View
            return (corpus,id2word)

        



        def create_model(self,corpus_id2word,vis):
            from pprint import pprint
            corpus=corpus_id2word[0]
            id2word=corpus_id2word[1]
            # number of topics
            num_topics =self.number_topics
            # Build LDA model
            self.lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=num_topics)
            # Print the Keyword in the 10 topics
            pprint(self.lda_model.print_topics())
            

            self.lda_model.save(self.model_path)
            
            
                
            
        

        def train_model(self,vis=False):
            corpus=self.prepare_data()
            self.create_model(corpus,vis)

        
        def predict_topics(self,data):
            lda_model = gensim.models.LdaModel.load(self.model_path)
            dictionary = corpora.Dictionary.load(self.id2word_path)
            topics_column=[]
            topics_percetage_column=[]
            
            bow_corpus = [dictionary.doc2bow(text) for text in data]

            # Get the topics for each document in the corpus
            document_topics = lda_model.get_document_topics(bow_corpus)

            # Iterate over each document's topics and print them
            for i, topics in enumerate(document_topics):
                current_perc4topics=[]
                current_topics=[]
                for t in range(0,len(topics)):
                     current_topic=topics[t]
                     topic=current_topic[0]
                     
                     percentage=current_topic[1]
                     current_perc4topics.append((topic,percentage))
                     current_topics.append(topic)
                     print("topic",current_topic)
                     print("perc",current_perc4topics)
                     


                topics_column.append(current_topics[:self.top_k_topics])
                topics_percetage_column.append(current_perc4topics[:self.top_k_topics])

            
            return [topics_column,topics_percetage_column]
                        

        def test(self):
            lda_model = gensim.models.LdaModel.load(self.model_path)
            dictionary = corpora.Dictionary.load(self.id2word_path)
                # Preprocess the new text
            new_text = "d3.js bar plot"
            new_text = new_text.lower().split()
            new_text_bow = dictionary.doc2bow(new_text)
    
            # Get the topics related to the new text
            topics = lda_model.get_document_topics(new_text_bow)

            # Print the topics
            for topic in topics:
                print("Topic {}: {:.2%}".format(topic[0], topic[1]))

     
if __name__=="__main__":
     model=LDAModel()
     #model.train_model()
     
     #individuo i topics per ogni frase

     '''
     data=pd.read_csv("index_csv_parsed.csv")
     
     text=data["parsed_text"].apply(lambda x: x.lower().split())
     
     predicted_topics=model.predict_topics(text)
     predicted_topics_col=predicted_topics[0]
     predicted_topics_perc=predicted_topics[1]
     data["topics"]=predicted_topics_col
     data["topics2perc"]=predicted_topics_perc

     data.to_csv("index_with_topics.csv",index=False)
     '''

     model.test()



