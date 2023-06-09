from PyPDF2 import PdfReader
import os
import json

class DataExtractor:

    def __init__(self):

        self.main_folder = os.path.join("../")

        self.PDF = "pdf"

        self.index = {}
        self.index_path = "index.json"

    def extract_data(self):

        for filename in os.listdir(self.main_folder):
            file_path = os.path.join(self.main_folder, filename)
            
            if os.path.isfile(file_path):

                extension = filename.split(".")[-1]

                if extension == self.PDF:
                    print("[READ]", filename)
                    self.index[filename] = self.extract_data_from_pdf(file_path)
        
        self.save_index()
    
    def extract_data_from_pdf(self, file):

        output = {}
        pdfObj = open(file, "rb")
        pdfReader = PdfReader(pdfObj)

        slide_number = 1
        for i in pdfReader.pages:

            text = i.extract_text().encode("cp1252").decode("utf8")
            output[slide_number] = text
            slide_number += 1

        pdfObj.close()
        return output

    def save_index(self):
        with open(self.index_path, "w", encoding="utf-8") as json_file:
            json.dump(self.index, json_file, indent = 4, sort_keys = True)


if __name__ == "__main__":
    dataExtractor = DataExtractor()
    dataExtractor.extract_data()
            