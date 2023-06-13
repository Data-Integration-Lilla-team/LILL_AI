
import os
from crawler import Crawler
from extractor_docx import DOCX_Text_Extractor
from extractor_PDF import PDF_Text_Extractor
from extractor_pptx import PPTX_Text_Extractor
from extractor_txt import TXT_Text_Extractor
import pandas as pd

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
        self.index_csv_path=r"dataExtraction\output\index_csv.csv"

    def save_index_csv(self):
        columns=["path","page","text"]
        data=[]
        for k in self.index:
            file_name_and_page=k.split("#")
            file_name=file_name_and_page[0]
            page_number=int(file_name_and_page[1])
            text=self.index[k]
            current_data=[file_name,page_number,text]
            data.append(current_data)

        data=pd.DataFrame(data=data,columns=columns)
        data = data.sort_values(by=['path', 'page'])
        
        data.to_csv(self.index_csv_path,index=False)  
    def save_index(self):
        with open(self.index_path, "w", encoding="utf8") as json_file:
            json.dump(self.index, json_file, indent=4, sort_keys=True, ensure_ascii=False)

    

    #utilizza il crawler per individuare i file da indicizzare
    def extract_data_new(self):
        self.crawler.crawl_1()
        
        
        files_to_elab=self.crawler.crawl_2()
        print(len(files_to_elab.fringe))
        values_ppt=dict()
        for k in files_to_elab.fringe.keys():
            if k=="pdf":
                
                values_pdf=self.PDF_extractor.extract_data(files_to_elab.fringe[k])
                
            elif k=="pptx":
                values_ppt=self.PPPT_extractor.extract_data(files_to_elab.fringe[k])
                
        self.index = values_pdf.copy()  # Create a copy of the first dictionary

        self.index.update(values_ppt)  # Update the copy with the second dictionary

        self.save_index() 

        self.save_index_csv()
        
        
            
           

                
    



if __name__=="__main__":
    dataExtractor=DataExtractor()
    dataExtractor.extract_data_new()
               
                    
                   




    

                
               
                    


'''pdfObj=open('id-00-presentazione-corso.pdf','rb')

pdfReader=PyPDF2.PdfFileReader(pdfObj)

pageObj=pdfReader.getPage(47)

print(pageObj.extractText())

pdfObj.close()
'''

