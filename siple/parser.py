

from siple.nlp import Model

class Parser:
    def __init__(self, model:Model = None) -> None:
        self._model = model 
        self.clear()
        
    def clear(self):
        self.input_text = ""
        self.verbs =[]

    def parse(self, text) -> list:
        self.clear()
        self.input_text = text
        self.verbs = self._model.parse(text.lower())
        return self.verbs