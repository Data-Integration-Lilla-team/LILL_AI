from PyPDF2 import PdfReader

class PDF_Text_Extractor:
    def __init__(self):
        pass

    def extract_data(self, list_of_path):
        print("Estrazione dati pdf")
        print(list_of_path)
        dict_path_dict_page_text = {}
        for file in list_of_path:
            print(file)
            dict_page_text = {}
            reader = PdfReader(file)
            n_pages = len(reader.pages)
            for i in range(n_pages):
                page = reader.pages[i]
                text = page.extract_text()
                dict_page_text[str(i)] = text
            dict_path_dict_page_text[file] = dict_page_text
        return dict_path_dict_page_text
