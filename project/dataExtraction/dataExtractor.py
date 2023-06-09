
import os
from crawler import Crawler
from extractor_docx import DOCX_Text_Extractor
from extractor_PDF import PDF_Text_Extractor
from extractor_pptx import PPTX_Text_Extractor
from extractor_txt import TXT_Text_Extractor

import json

class DataExtractor:

    def __init__(self):

        #crawler  
        self.crawler=Crawler()

        #moduli per l'estrazione del testo dai diversi formati files
        self.PDF_extractor=PDF_Text_Extractor()
        
        self.PPPT_extractor=PPTX_Text_Extractor()
        self.DOCX_extractor=DOCX_Text_Extractor()
        self.TXT_extractor=TXT_Text_Extractor()

        self.index={}
        self.index_path="index.json"
        
    def save_index(self):
        with open(self.index_path, "w", encoding="utf8") as json_file:
            json.dump(self.index, json_file, indent=4, sort_keys=True, ensure_ascii=False)

    def extract_data_old(self):
        for filename in os.listdir(self.public_folder):
            file_path = os.path.join(self.public_folder, filename)
            
            if os.path.isfile(file_path):
            
                if self.EXTENSIONS not in filename:
                    filename=self.converter.convert_into_PDF(filename,file_path,self.public_folder)
                    print("[CONVERITTO]",filename)
                else:
                    print("[NON CONVERTITO]",filename)

                print("[START]",filename)
                self.index[filename]=self.extract_data_from_pdf(file_path)
                print("[FINISH]",filename+"\n")

        
        self.save_index()

    #utilizza il crawler per individuare i file da indicizzare
    def extract_data_new(self):
        files_to_elab=self.crawler.crawl()
        for k in files_to_elab.fringe.keys():
            if k=="pdf":
                
                self.PDF_extractor.extract_data(files_to_elab.fringe[k])
            elif k=="pptx":
                self.PPPT_extractor.extract_data(files_to_elab.fringe[k])
            
            elif k=="docx":
                self.DOCX_extractor.extract_data(files_to_elab.fringe[k])

            else:
                self.TXT_extractor.extract_data(files_to_elab.fringe[k])
        

                
    



if __name__=="__main__":
    dataExtractor=DataExtractor()
    dataExtractor.extract_data_new()
               
                    
                   




    

                
               
                    


'''pdfObj=open('id-00-presentazione-corso.pdf','rb')

pdfReader=PyPDF2.PdfFileReader(pdfObj)

pageObj=pdfReader.getPage(47)

print(pageObj.extractText())

pdfObj.close()
'''

