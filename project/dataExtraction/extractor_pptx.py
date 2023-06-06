from pptx import Presentation

class PPTX_Text_Extractor:
    def __init__(self):
        pass

    def extract_data(self, list_of_path):
        print("Estrazione dati pptx")
        dict_path_dict_page_text = {}
        for file in list_of_path:
            dict_page_text = {}
            presentation = Presentation(file)
            for idx, slide in enumerate(presentation.slides):
                text = ""
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text
                dict_page_text[str(idx)] = text
            dict_path_dict_page_text[file] = dict_page_text
        return dict_path_dict_page_text