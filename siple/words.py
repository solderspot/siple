
from siple.nlp.model import Model
from enum import Enum, auto

class WordType(Enum):
    UNKNOWN = "unkn"
    VERB = "verb"
    PREPOSITION = "prep"
    ADVERB = "advb"
    NOUN = "noun"
    PRONOUN = "pron"
    ADJECTIVE = "adjt"
    PARTICLE = "part"
    
    def __str__(self):
        return self.value

    @classmethod
    def from_string(cls, string):
        for word_type in cls:
            if word_type.value == string:
                return word_type
        return cls.UNKNOWN

class Word:
    """
    A class to represent a word.
    
    text     : str      - the text of the word.
    vector   : vector   - the vector representation of the word.
    childern : list     - list of child words related to this word.
    type     : WordType - the type of the word.
    """
    def __init__(self, text:str, type:WordType = WordType.UNKNOWN):
        self.text = text.lower()
        self.vector = None
        self.type = type
        self.childern = []
        
    def __str__(self):
        return self.text
    
    def __repr__(self):
        return self.text
    
    def __hash__(self):
        return hash(self.text)

    def add(self, child):
        if not isinstance(child, Word):
            raise ValueError("Invalid type for child - must be Word")   
        if child.hasChild(self):
            raise ValueError("Circular reference detected")         
        self.childern.append(child)    
        
    def hasChild(self, child):
        return child in self.childern or any([c.hasChild(child) for c in self.childern])
    
    def clearChildren(self):
        self.childern = []
        
    def printTree(self, level=0):
        print("  "*level, f"{self.text} - ({self.type})")
        for child in self.childern:
            child.printTree(level+1)
        
class Words:
    """
    A class to represent a list of "Word"s.
    
    If the class is initialized with a NLPModel, the word vectors will be automatically generated.
    
    list : list - list of Word objects.
    map  : dict - a map of text to Word objects
    """
    
    def __init__(self, model:Model = None):
        """
        Constructor for Words class.

        Args:
            model (NLPModel, optional): NLP Model to use. Defaults to None.
        """
        self.clear()
        self.__model = model
        
    def setModel(self, model:Model):
        """
        Set the NLP Model to be used.

        Args:
            model (NLPModel): The NLP Model to be used.
        """
        if self.__model is model:
            return
        self.__model = model
        self._recalculateVectors()
        
    def model(self) -> Model:
        """Get the NLP Model used.

        Returns:
            NLPModel: The NLP Model used.
        """
        return self.__model

    def clear(self):
        self.list = []
        self.vectors = []
        self.map = {}

    def add(self, item):
        """
        Add word(s) to the list.
        
        Item can be a string, a Word object, or a list of strings or Word objects.
        Each word in a string will be added as a separate word.
        If a word is already in the list, it will not be added again.

        Args:
            item (string or Word or list): The word to be added, either as a string or a Word object or a list.
        """
        # check for list
        if isinstance(item, list):
            self.__addArray(item)
            return
        
        # check for string
        if isinstance(item, str):
            self.__addString(item)
            return
        
        # check if not a Word
        if not isinstance(item, Word):
            raise ValueError("Invalid type for item - must be string or Word, or list of strings or Words")
        
        # check if already in list
        if item.text in self.map:
            return
        
        # update the vector
        item.vector = self.__model.wordVector(item.text) if self.__model is not None else None

        #add to list
        self.list.append(item)
        self.vectors.append(item.vector)
        self.map[item.text] = item        
                        
    def wordWithText(self, text:str):
        """Return the Word object which matched the given text.

        Args:
            text (string): The text of the Word to be searched for.

        Returns:
            Word: The word object if found, None otherwise.
        """
        return self.map.get(text.lower(), None)
    
    def wordsClosestTo(self, text:str, threshold=0.3):
        """
        Returns a list of words that are similar to the given text.
        The list is ordered by similarity score in descending order.
         

        Args:
            text (string): text of word to be searched for.
            threshold (float, optional): Similarity threshold. Defaults to 0.3.

        Returns:
            [ (word, similarity), ... )]: Array of tuples containing the word object and the similarity score.
        """
        if self.__model is None:
            return []
        vector = text if self.__model.isVector(text) else self.__model.wordVector(text)
        return self.wordsClosestToVector(vector, threshold)
                        
    def wordsClosestToVector(self, vector, threshold=0.3):
        """
        Returns a list of words that are similar to the given vector.
        The list is ordered by similarity score in descending order.
         
        Args:
            vector (Model vector): text of word to be searched for.
            threshold (float, optional): Similarity threshold. Defaults to 0.3.

        Returns:
            [ (word, similarity), ... )]: Array of tuples containing the word object and the similarity score.
        """
        
        # check if model is available
        if self.__model is None:
            # return empty list
            return []
                
        # Compute cosine similarity between the reference vector and all word vectors
        similarity_matrix = self.__model.compare_vectors([vector], self.vectors)[0]

        # Filter words based on the similarity threshold
        matched_words = [
            (word, similarity)
            for word, similarity in zip(self.list, similarity_matrix)
            if similarity > threshold
        ]
        
        # Sort by similarity score
        matched_words.sort(key=lambda x: x[1], reverse=True)
        return matched_words


    # private methods
    
    def __addString(self, string:str):
        texts = string.split()
        for text in texts:
            self.add(Word(text))

    def __addArray(self, array:list):
        for item in array:
            self.add(item)
            
    def _recalculateVectors(self):
        self.vectors = []
        for word in self.list:
            word.vector = self.__model.wordVector(word.text) if self.__model is not None else None
            self.vectors.append(word.vector)
