
from .words import Words
from siple.nlp import Model

class WordGroup:
    def __init__(self, model: Model = None ) -> None:
        self.words = Words(model)
        self.__model = model
        self.__name = None
        
    def setModel(self, model:Model):
        if self.__model is model:
            return
        self.__model = model
        self.words.setModel(model)
        
    def model(self) -> Model:
        return self.__model
        
    def setWords(self, words):
        self.words.clear()
        self.words.add(words)
        
    def name(self) -> str:
        if self.__name is not None:
            return self.__name
        return self.words.list[0].text if len(self.words.list) > 0 else ""
    
    def setName(self, name:str):
        self.__name = name
        
class WordGroups:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    def __init__(self, name:str, model:Model = None ):
        self.__model = model
        self.__name = name
        self.clear()

    def clear(self):
        self.list = []
        self.map = {}
        
    def setModel(self, model:Model):
        if self.__model is model:
            return
        self.__model = model
        for group in self.list:
            group.setModel(model)
        
    def model(self) -> Model:
        return self.__model
    
    def name(self) -> str:
        return self.__name
            
    def add(self, item):
        if isinstance(item, list):
            for i in item:
                self.add(i)
            return
        if isinstance(item, str):
            self.__addString(item)
            return
        if isinstance(item, tuple):
            self.__addTuple(item)
            return
        if isinstance(item, WordGroup):
            self.__addGroup(item)
                
    
    # private methods
    
    def __addString(self, string):
        if len(string) == 0:
            return
        group = WordGroup(self.__model)
        group.setWords(string)
        self.__addGroup(group)
        
    def __addTuple(self, tuple):
        if len(tuple) != 2:
            raise ValueError("tuple must have two elements - name and words")
        group = WordGroup(self.__model)
        group.setName(tuple[0])
        group.setWords(tuple[1])
        self.__addGroup(group)

    def __addGroup(self, group:WordGroup):
        if group in self.list:
            return
        # check that the words are not already assigned to another group
        for word in group.words.list:
            if word.text in self.map:
                raise ValueError(f"word '{word.text}' already assigned to a word group")
            else:
                self.map[word.text] = group
        group.setModel(self.__model)
        self.list.append(group)