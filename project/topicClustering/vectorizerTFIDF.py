import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
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

def get_list_of_docs(data):
    out=[]
    for k in data.keys():
        current_docs=data[k]
        current_docs=current_docs[2:]
        out.extend(current_docs)
    return out

data=load_data("index_parsed.json")

vectorizer=TfidfVectorizer( lowercase=True,         #trasforma tutto in lowercase
                           max_features=100,        #
                           max_df=0.8,              #elimina words aventi document freq > 0.8 (presenti nel 80% dei documenti)
                           min_df=5,                #ignora parole che non hanno almeno 5 occorrenze    
                           ngram_range=(1,3),       #crea tre indici, 1gram, 2gram, 3gram
                           

                            )

list_of_docs=get_list_of_docs(data)
vectors=vectorizer.fit_transform(list_of_docs)
feature_names=vectorizer.get_feature_names_out()

dense=vectors.todense()
denselist=dense.tolist()

#indivudua le keywords per ogni pagina
all_keywords=[]
for doc in denselist:
    x=0
    keywords=[]
    for word in doc:
        if word > 0:
            keywords.append(feature_names[x])
        x+=1
    all_keywords.append(keywords)   
    
#clusterizzazione in base alle keywords mediante kmeans
true_k=5   #numero di cluster
model=KMeans(n_clusters=true_k,init="k-means++",max_iter=100,n_init=1)
model.fit(vectors)


#centoridi
order_centroids=model.cluster_centers_.argsort()[:,::-1]
terms=vectorizer.get_feature_names_out()

#memorizzo i centroidi
with open("topicClustering/trc_result.txt","w",encoding="utf-8") as f:
    for i in range(true_k):
        f.write(f"Clusters {i}")
        f.write("\n")
        for ind in order_centroids[i,:10]: #prendi le prime 10 keywords
            f.write(" %s" % terms[ind],)
            f.write("\n")
        f.write("\n\n")


#==============PLOTTING====================
import matplotlib.pyplot as plt
from sklearn.decomposition import KernelPCA

kmeans_index=model.fit_predict(vectors)

pca=KernelPCA(n_components=2)
scatter_plot=pca.fit_transform(vectors.toarray())

colors=["r","b","c","y","m"]
x_axis=[o[0] for o in scatter_plot]
y_axis=[o[1] for o in scatter_plot]


fig,ax=plt.subplots(figsize=(50,50))

ax.scatter(x_axis,y_axis,c=[colors[d] for d in kmeans_index])

plt.savefig("topicClustering/clusters.png")