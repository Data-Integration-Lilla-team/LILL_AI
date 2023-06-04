import PyPDF2
import os
from fileConverter import FileConverter

import json

class DataExtractor:

    def __init__(self):
          
        self.public_folder="dataExtraction\data_test\public"
        self.private_folder="dataExtraction\data_test\protected"
        self.EXTENSIONS=".pdf"
        self.converter=FileConverter()
        self.index={}
        self.index_path="index.json"
    
    def extract_data_from_pdf(self,file):

        output=dict()
        pdfObj=open(file,'rb',encoding="ISO")

        pdfReader=PyPDF2.PdfReader(pdfObj)

        
        slide_number=1
        for i in pdfReader.pages:

            text=i.extract_text()
            output[slide_number]=text
            slide_number+=1



        

        pdfObj.close()
        return output

    def save_index(self):
        with open(self.index_path, "w") as json_file:
            json.dump(self.index, json_file,indent=4, sort_keys=True)

    def extract_data(self):
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

                

            
                





if __name__=="__main__":
    dataExtractor=DataExtractor()
    dataExtractor.extract_data()
               
                    
                   




    

                
               
                    


'''pdfObj=open('id-00-presentazione-corso.pdf','rb')

pdfReader=PyPDF2.PdfFileReader(pdfObj)

pageObj=pdfReader.getPage(47)

print(pageObj.extractText())

pdfObj.close()
'''

