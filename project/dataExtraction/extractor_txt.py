
class TXT_Text_Extractor:
    def __init__(self):
        pass

    def extract_data(self, list_of_path):
        print("Estrazione dati txt")
        dict_path_dict_page_text = {}
        for file in list_of_path:
            f = open(file, "r")
            text = f.read()
            f.close()
            dict_path_dict_page_text[file] = {"0": text}
        return dict_path_dict_page_text