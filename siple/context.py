
from siple import WordGroups
from siple.objects import Objects
from siple.nlp.model import Model

class Context:
    def __init__(self, model:Model):
        self.__model = model
        self.modifiers = WordGroups('Modifiers', model)
        self.actions = WordGroups('Actions', model)
        self.prepositions = WordGroups('Prepositions', model)
        self.objects = Objects(model)
        
    def model(self) -> Model:
        return self.__model
    
    def setModel(self, model:Model):
        if self.__model is model:
            return
        self.__model = model
        self.modifiers.setModel(model)
        self.actions.setModel(model)
        self.prepositions.setModel(model)
        self.objects.setModel(model)
        
    def clear(self):
        self.modifiers.clear()
        self.objects.clear()
        self.actions.clear()
        self.prepositions.clear()
        
    def addModifiers(self, list ):
        self.modifiers.add(list)
    
    def addObjects(self, list ):
        self.objects.add(list)
        
    def addActions(self, list ):
        self.actions.add(list)
        
    def addPrepositions(self, list ):
        self.prepositions.add(list)