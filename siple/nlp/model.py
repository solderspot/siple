from abc import ABC, abstractmethod

class Model(ABC):
    
    def __init__(self) -> None:
        super().__init__()
        self.zeroVector = None
    
    @abstractmethod
    def parse(self, text) -> list:
        pass
    
    @abstractmethod
    def wordVector(self, text):
        pass
    
    @abstractmethod
    def meanOfVectors(self, vectors):
        pass
    
    @abstractmethod
    def compare_vectors(self, vectors1, vectors2):
        pass
    
    @abstractmethod
    def isZeroVector(self, vector):
        pass

    @abstractmethod
    def isVector(self, item):
        pass
    
    def meanOfWords(self, words):
        return self.meanOfVectors([word.vector for word in words if word.vector is not None])