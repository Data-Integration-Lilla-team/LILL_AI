'''
Crawler logic
Partendo da un direttorio seed, il crawler accede ricorsivamente nelle cartelle individuando nuovi file (file che non hanno subito il processo di tockenizzazione).
Definiamo nuovi file, file per il quale:
1. non sono stati indicizzati
2. hanno subito una modifica dopo l'indicizzazione

Il lavoro del crawler può esser sintetizzato nel seguente modo:
1. partendo da rootfolder crea un file json in cui, per ogni sottocartella memorizza i file associati (topologia.json)
    ogni file ha due variabili associate: lastUpdate, boolean (True se è nuovo, False altrimenti)

2. Il crawler utilizza il file topologia.json per individuare nuove pagine (aventi il  booleano a True) e li inserisce in una Fringe 

3. La fringe suddivide i file in base all'estensione (in quanto subiranno un processo diverso di estrazione dati). Per ogni tipologia di estensione, assocaimo la lista di file
che devono essere elaborati (es. {pdf: [pathFile1,pathFile2...]})

4. Il crawler passa la fringe creata al modulo Data Extraction

NOTA
Al primo run, il crawler analizza tutti i file
Nei run successivi (periodici), il crawler passerà al dataExtractor solo i nuovi file


NOTA 2
La fase di creazione della topolgia e di ricerca dei nuovi file da indicizzare è distaccata per scelta
'''


import os
import time
import json
import shutil




#classe fringe di supporto
#é un dizionario composto da 4 entry
#1. lista di file .pdf da indicizzare
#2. lista di file .txt da indicizzare
#3. lista di file .pptx da indicizzare
#4. lista di file .docx da indicizzare
class Fringe:
    def __init__(self):
          self.fringe={"pdf":[],"pptx":[]}   #lista di file da indicizzare

    def add_elements(self, list,root):
         for k in list.keys():
            if list[k][1]==True:
                file_name=os.path.join(root,k)
               
                extension=k.split(".")
                extension=extension[len(extension)-1]
                self.fringe[extension].append(file_name)
                
class Crawler:
    def __init__(self) -> None:
        self.rootFolder = os.path.join("dataExtraction", "data_test", "rootfolder")
        self.extensions=set(["pdf","pptx"])
        self.dir_topology=os.path.join("topology.json")
        self.file_to_index=os.path.join("file_to_index.json")
        


    #Metodo per la lettura del file topology.json in cui è memorizzata la stuttura del direttorio
    #Se non esiste (primo run) restituisce una mappa vuota
    def get_topology(self):
        try:
            with open(self.dir_topology, "r") as file:
                # Load the JSON data into a dictionary
                data = json.load(file)
                
        except FileNotFoundError:
                data=dict()
        return data


    #Verifica dei file da indicizzare (considera sia nuovi file, sia file indicizzati che hanno subito una modifica (file obsoleti))
    def check_updateV2(self,files,root,entry):
        new_file_name=entry[0]      #nome del file
        last_update=entry[1]        #ultima modifica
        
        # se il file è nuovo, allor deve essere indicizzato
        if new_file_name not in files[root]:
             files[root][new_file_name]=[last_update,True]
        
        # se il file è gia presente, verifico la data di ultima modifica
        else:
            
             old_last_update=files[root][new_file_name]
             if last_update > old_last_update:
                  files[root][new_file_name]=[last_update,True]
             else:
                  files[root][new_file_name]=[last_update,False]
    

    #Condisera solo la presenza del file e non l'ultimo aggiornamento
    def check_update(self,files,root,entry):
        new_file_name=entry[0]
        last_update=entry[1]
        

        if new_file_name not in files[root]:
             files[root][new_file_name]=[last_update,True]
        
                  
    #Metodo di creazione ed aggiornamento del file topology.json (al primo run lo crea, negli altri lo aggiorna inserendo i nuovi file)
    def gather_paths(self):
        matched_files = self.get_topology()
        
        for root, dirs, files in os.walk(self.rootFolder):

            #per ogni directory in modo ricorsivo accedo ai file 
            if root not in matched_files:
                matched_files[root]=dict()

            #per ogni file individuato
            for file in files:
               
                extension=file.split(".")
                extension=extension[len(extension)-1]
                #se l'estensione del file è gestibile (pdf, pptx, docx, text)
                if extension in self.extensions:
                    modification_date=os.path.getatime(os.path.join(root,file))
                    last_modification_date = time.ctime(modification_date)
                    entry=(file,last_modification_date)
                    self.check_update(matched_files,root,entry)
                    
        return matched_files

    #Memorizzazione del fiele topology.pdf
    def print_topology(self,matched_files):
       
            with open(self.dir_topology, "w") as json_file:
                json.dump(matched_files, json_file,indent=4, sort_keys=True)


    #Metodo di ricerca dei file da aggiornare. Per ogni sottocartella di root, accedo ai file e verifico il campo boolean
    def check_new_files(self,data,root):
        out=[]
        for k in data.keys():
            if data[k][1]==True:
                file_name=os.path.join(root,k)
                out.append(file_name)
        
        return out
                
    #Metodo di creazione dell'output (fringe)
    #A partire dal file topology.json inserisce in fringe i nuovi file
    #Fringe provede a smistarli nella pipeline giusta
    def create_list_new_files(self):
        fringe=Fringe()
        with open(self.dir_topology,"r") as file:
            data=json.load(file)
        
        for k in data.keys():
            files_in_k=data[k]
            fringe.add_elements(files_in_k,k)
        
        return fringe

    
         



#metodo di test che simula l'inserimento da parte dell'utente di nuovi file
#Metodo principale.
    #Si susseguono: 1. Creazione, aggiornamento topology.json
    #               2. Individuazione nuovi file
    def crawl_1(self):
         topology=self.gather_paths()
         self.print_topology(topology)
        
    
    def crawl_2(self):
        new_files=self.create_list_new_files()
        return new_files
    
    
   