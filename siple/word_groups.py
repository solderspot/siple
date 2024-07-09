
from .words import Words
from siple.nlp import Model

class WordGroup:
    """ A WordGroup is a Words with a name. If no name is set, the first word is used as the name.
    
        You can specify a model in the constructor or later with setModel().
    
        - wg = WordGroup(<model:optional>)
        - wg.setWords(<words>) - set words
        - wg.words() - Words
        - wg.setModel(<model>) - set model
        - wg.setName(<name>) - set name
        - wg.name() - name
    """
    def __init__(self, model: Model = None ) -> None:
        self.__words = Words(model)
        self.__model = model
        self.__name = None
        
    def setModel(self, model:Model):
        if self.__model is model:
            return
        self.__model = model
        self.__words.setModel(model)
        
    def model(self) -> Model:
        return self.__model
    
    def words(self) -> Words:
        return self.__words
        
    def setWords(self, words):
        self.__words.clear()
        self.__words.add(words)

    def addWords(self, words):
        self.__words.add(words)
        
    def name(self) -> str:
        if self.__name is not None:
            return self.__name
        return self.__words.list[0].text if len(self.__words.list) > 0 else ""
    
    def setName(self, name:str):
        self.__name = name
        
class WordGroups:        
    """ WordGroups is list of WordGroup's with a name. Name is specified in the constructor.
        
        All words in all groups must be unique. If a word is already assigned to a group, an error is raised.
        
        - wgs = WorkGroups(<name>, <model:optional>)
        - wgs.add(<group>) - add to list
        - wgs.list(): list of WordGroup
        - wgs.clear() - clear list
        - wgs.setModel(model) - set model for all groups
    """                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    def __init__(self, name:str, model:Model = None ):
        self.__model = model
        self.__name = name
        self.clear()

    def clear(self):
        self.__list = []
        self.__map = {}
        
    def setModel(self, model:Model):
        if self.__model is model:
            return
        self.__model = model
        for group in self.__list:
            group.setModel(model)
        
    def model(self) -> Model:
        return self.__model
    
    def name(self) -> str:
        return self.__name
    
    def list(self) -> list:
        return self.__list
                
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
        if group in self.__list:
            return
        # check that the words are not already assigned to another group
        for word in group.words().list:
            if word.text in self.__map:
                raise ValueError(f"word '{word.text}' already assigned to a word group")
            else:
                self.__map[word.text] = group
        group.setModel(self.__model)
        self.__list.append(group)