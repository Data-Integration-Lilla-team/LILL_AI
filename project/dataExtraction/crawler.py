import os
import time
import json

class Crawler:
    def __init__(self) -> None:
        self.rootFolder=r"dataExtraction\data_test\rootfolder"
        self.extensions=set(["pdf","txt","pptx","docx"])
        self.dir_topology=r"topology.json"
        self.file_to_index=r"file_to_index.json"
        


    #acquisizione della topologia corrente del direttorio root
    def get_topology(self):
        try:
            with open(self.dir_topology, "r") as file:
                # Load the JSON data into a dictionary
                data = json.load(file)
                
        except FileNotFoundError:
                data=dict()
        return data


    #considera: presenza del file + ultimo aggiornamento
    def check_updateV2(self,files,root,entry):
        new_file_name=entry[0]
        last_update=entry[1]
        

        if new_file_name not in files[root]:
             files[root][new_file_name]=[last_update,True]
        
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
        
                  
    #individuazione file da indicizzare
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

    def print_topology(self,matched_files):
       
            with open(self.dir_topology, "w") as json_file:
                json.dump(matched_files, json_file,indent=4, sort_keys=True)

def update_topology(path):
    with open(path, "r") as file:
        # Load the JSON data into a dictionary
        data = json.load(file)
    
    for dirs in data.keys():
         if len(data[dirs])>=1:
              files=data[dirs]
              for file in files.keys():
                   files[file][1]=False
    
    with open(path,"w") as file:
         json.dump(data, file,indent=4, sort_keys=True)
                   
     
if __name__=="__main__":

   

    crawler=Crawler()
    matched_files=crawler.gather_paths()    # Print the matched file paths
    crawler.print_topology(matched_files)
    
    #Alla prima creazione tutti i file sono da indicizzare
    #Una volta indicizzati il valore boolean associato passa a false
    #Il meotodo sotto è una simulazione della modifica del paramentro
    #update_topology(crawler.dir_topology)
    
    
   