'''
Classe specializzata nella conversione di file che non sono pdf in pdf.
Viene invocato il metodo convert_pdf ogni qualvolta il dataExtractor trova un file non .pdf
'''

import os

class FileConverter:
    
    def __init__(self) -> None:
        self.EXTENSION=".pdf"

    def createName(self,file_name_parts,base_path):
        out=""
        cont=0
        for i in range(0,len(file_name_parts)):
                if cont==(len(file_name_parts)-1):
                    out+=file_name_parts[i]
                else:
                    out+=file_name_parts[i]+"."
        
        out=os.path.join(base_path,out)
        return out
    

    def convert_into_PDF(self, old_name, old_path,base_path):
        words=old_name.split(".")
                    
                    
       #modifico l'estensione
        words[len(words)-1]="pdf"

                    #creo il nuovo nome
        new_fileName=self.createName(words,base_path)
                    
                    #rinomino il file
        os.rename(old_path,new_fileName)

        return new_fileName
    '''
    def convert_PPTX_to_PDF(self,pptx_path,pdf_path):
        pptx_file = os.path.abspath(pptx_path)
        pdf_file = os.path.abspath(pdf_path)

        powerpoint = CreateObject("Powerpoint.Application")
        powerpoint.Visible = 1

        presentation = powerpoint.Presentations.Open(pptx_file)
        presentation.SaveAs(pdf_file, PPtSaveFormat.PDF)

        presentation.Close()
        powerpoint.Quit()
    '''
         