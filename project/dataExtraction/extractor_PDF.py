from PyPDF2 import PdfReader

class PDF_Text_Extractor:

    def __init__(self):
        pass


    def extract_data(self, list_of_path):
        print("Estrazione dati pdf")
        print(list_of_path)
        dict_path_page_text = {}
        for file in list_of_path:
            print(file)
            reader = PdfReader(file)
            n_pages = len(reader.pages)
            for i in range(n_pages):
                page = reader.pages[i]
                text = page.extract_text()
                key = file + "#" + str(i)
                dict_path_page_text[key] = text
        return dict_path_page_text
