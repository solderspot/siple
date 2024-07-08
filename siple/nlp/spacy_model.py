import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from siple import Word, WordType, Model


# Define word_type_map outside the function
_word_type_map = {
    "VERB": WordType.VERB,
    "NOUN": WordType.NOUN,
    "ADJ": WordType.ADJECTIVE,
    "ADV": WordType.ADVERB,
    "ADP": WordType.PREPOSITION,
    "PRON": WordType.PRONOUN,
}

class SpacyModel(Model):
    
    def __init__(self, model_name = None ) -> None:
        super().__init__()
        name = model_name if model_name is not None else "en_core_web_md"
        self._nlp = spacy.load(name)
        self._vocab = self._nlp.vocab
        if self._vocab.vectors_length == 0:
            raise ValueError("The loaded spaCy model does not contain word vectors.")
        self.zeroVector = np.zeros(self._vocab.vectors_length)
        self._word_map = {}
        self._verb_deps = {"nsubj", "dobj", "prep", "advmod", "prt", "dative", "xcomp", "npadvmod"}
        self._noun_deps = {"amod", "prep", "compound", "aux"}
            
    def parse(self, text) -> list:
        doc = self._nlp(text)
        verbs = []
        self._reset()
        
        # find all the verbs in the sentence
        for token in doc:
            if token.dep_ == "ROOT":
                verbs.append(self._new_word(token))

        if len(verbs) == 0:
            return verbs # no verbs found

        # build the word tree
        for token in doc:
            
            word = self._get_word(token)            
            if word in verbs:
                continue
            
            parent = self._get_word(token.head)
            
            if parent.type == WordType.VERB:
                if token.dep_ in self._verb_deps:
                    parent.add(word)
            elif parent.type == WordType.NOUN:
                if token.dep_ in self._noun_deps:
                    if word.type == WordType.PREPOSITION:
                        # we want to move prepositions to the root
                        verb_token = self._get_verb(token.head)
                        if verb_token is None:
                            parent.add(word)
                        else:
                            verb = self._get_word(verb_token)
                            verb.add(word)
                    else:
                        parent.add(word)
            elif parent.type == WordType.PREPOSITION:
                if token.dep_ == "pobj":
                    parent.add(word)

        return verbs

    def wordVector(self, word):
        found = self._vocab[word]
        if found is not None:
            return found.vector
        return self.zeroVector
    
    def compare_vectors(self, vectors1, vectors2):
        return cosine_similarity(vectors1, vectors2)
    
    def isZeroVector(self, vector):
        return vector is self.zeroVector or np.array_equal(vector, self.zeroVector)
    
    def isVector(self, item):
        return isinstance(item, np.ndarray)
    
    def meanOfVectors(self, vectors):
        return np.mean(vectors, axis=0) if vectors and len(vectors) > 0 else self.zeroVector
    

    # private methods
    
    def _reset(self):
        self._word_map = {}
        
    def _new_word(self, token):
        if token.dep_ == 'prt':
            word_type = WordType.PARTICLE
        elif token.dep_ == 'amod':
            word_type = WordType.ADJECTIVE
        elif token.dep_ == 'compound':
            word_type = WordType.ADJECTIVE
        else:
            word_type = _word_type_map.get(token.pos_, WordType.UNKNOWN)
    
        word = Word(token.text, word_type)
        self._word_map[token] = word
        return word
    
    def _get_word(self, token):
        return self._word_map.get(token) or self._new_word(token)
    
    def _get_verb(self, token):
        if token is None:
            return None
        if token.dep_ == "ROOT":
            return token
        return self._get_verb(token.head)
