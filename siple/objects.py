
from .words import Words
from siple.nlp import Model

class Object:
    def __init__(self, model:Model=None ):
        self.adjectives = Words(model)
        self.nouns = Words(model)
        self.__model = model
        
    def setModel(self, model:Model):
        if self.__model is model:
            return
        self.__model = model
        self.adjectives.setModel(model)
        self.nouns.setModel(model)
        
    def model(self) -> Model:
        return self.__model
        
    def setAdjectives(self, adjectives):
        self.adjectives.clear()
        self.adjectives.add(adjectives)

    def setNouns(self, nouns):
        self.nouns.clear()
        self.nouns.add(nouns)
        
    def name(self) -> str:
        return self.nouns.list[0].text if len(self.nouns.list) > 0 else ""
        
class Objects:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    def __init__(self, model:Model = None ):
        self.__model = model

    def clear(self):
        self.list = []
        
    def setModel(self, model:Model):
        if self.__model is model:
            return
        self.__model = model
        for obj in self.list:
            obj.setModel(model)
        
    def model(self) -> Model:
        return self.__model
            
    def add(self, item):
        if isinstance(item, list):
            self.__addArray(item)
            return
        if isinstance(item, str):
            self.__addString(item)
            return
        if isinstance(item, tuple):
            self.__addTuple(item)
            return
        if isinstance(item, Object):
            item.setModel(self.__model)
            self.list.append(item)
                
    
    # private methods
    
    def __addString(self, string):
        texts = string.split()
        if len(texts) == 0:
            return
        # the last word is the noun
        noun = texts.pop()
        obj = Object(self.__model)
        obj.nouns.add(noun)
        obj.adjectives.add(texts)
        self.list.append(obj)
        
    def __addArray(self, array):
        for item in array:
            self.add(item)
            
    def __addTuple(self, item):
        if len(item) != 2:
            raise ValueError("Tuple must have 2 elements, string of adjectives and string of nouns.")
        obj = Object(self.__model)
        obj.nouns.add(item[1])
        obj.adjectives.add(item[0])
        self.list.append(obj)

