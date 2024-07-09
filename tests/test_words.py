import unittest
from siple import Words, Word, WordType
from test.spacy import spacyModel

class TestWord(unittest.TestCase):
    
    def test_create(self):
        word = Word('test')
        self.assertEqual(word.text, 'test')
        self.assertIsNone(word.vector)
        
    def test_add_child(self):
        word = Word('test')
        child = Word('child')
        
        word.add(child)
        self.assertTrue(word.hasChild(child))
        
        child2 = Word('child2')
        child.add(child2)
        self.assertTrue(word.hasChild(child2))
        
        child3 = Word('child3')
        child2.add(child3)
        self.assertTrue(word.hasChild(child3))
        
        with self.assertRaises(ValueError) as context:
            child3.add(word)
        self.assertEqual(str(context.exception), "Circular reference detected")
        
        with self.assertRaises(ValueError) as context:
            word.add('child')
        self.assertEqual(str(context.exception), "Invalid type for child - must be Word")
        
    def test_clear_children(self):
        word = Word('test')
        child = Word('child')
        word.add(child)
        self.assertTrue(word.hasChild(child))
        
        word.clearChildren()
        self.assertFalse(word.hasChild(child))
        
    def test_word_type(self):
        word = Word('test', WordType.NOUN)
        self.assertEqual(word.type, WordType.NOUN)
        self.assertEqual(str(word.type), 'noun')
        
        word = Word('test', WordType.VERB)
        self.assertEqual(word.type, WordType.VERB)
        self.assertEqual(str(word.type), 'verb')
        
        word = Word('test', WordType.ADJECTIVE)
        self.assertEqual(word.type, WordType.ADJECTIVE)
        self.assertEqual(str(word.type), 'adjt')
        
        word = Word('test', WordType.ADVERB)
        self.assertEqual(word.type, WordType.ADVERB)
        self.assertEqual(str(word.type), 'advb')
        
        word = Word('test', WordType.PREPOSITION)
        self.assertEqual(word.type, WordType.PREPOSITION)
        self.assertEqual(str(word.type), 'prep')

        word = Word('test', WordType.PARTICLE)
        self.assertEqual(word.type, WordType.PARTICLE)
        self.assertEqual(str(word.type), 'part')
        
        word = Word('test')
        self.assertEqual(word.type, WordType.UNKNOWN)
        self.assertEqual(str(word.type), 'unkn')
        
        self.assertEqual(WordType.from_string('verb'), WordType.VERB)
        self.assertEqual(WordType.from_string('noun'), WordType.NOUN)
        self.assertEqual(WordType.from_string('adjt'), WordType.ADJECTIVE)
        self.assertEqual(WordType.from_string('advb'), WordType.ADVERB)
        self.assertEqual(WordType.from_string('prep'), WordType.PREPOSITION)
        self.assertEqual(WordType.from_string('unkn'), WordType.UNKNOWN)
        self.assertEqual(WordType.from_string('sdfsdfsdf'), WordType.UNKNOWN)
        self.assertEqual(WordType.from_string('part'), WordType.PARTICLE)
        
class TestWords(unittest.TestCase):
        
    def assertListSize(self, words, size):
        self.assertEqual(len(words.list), size)
        self.assertEqual(len(words.map), size)
        self.assertEqual(len(words.vectors), size)
    
    def test_empty_words(self):
        words = Words()
        self.assertListSize(words, 0)
           
    def test_add_word(self):
        words = Words()
        word = Word('test')
        
        words.add(word)
        self.assertListSize(words, 1)
        
        words.add(word)
        self.assertListSize(words, 1)
        
        words.add(Word('test2'))
        self.assertListSize(words, 2)
        
        words.clear()
        self.assertListSize(words, 0)       

    def test_add_word_string(self):   
        words = Words()
        words.add('test')
        
        self.assertListSize(words, 1)
        self.assertEqual(words.list[0].text, 'test')
        
        words.clear()
        
        words.add('test test2 test abc')
        self.assertListSize(words, 3)
        self.assertEqual( words.wordWithText('abc').text, 'abc')
        
        words.clear()
        words.add( ['dog', 'cat mouse iceberg', Word('test'), ['dog', Word('test'), 'string']])
        self.assertListSize(words, 6)
        self.assertEqual( words.wordWithText('String').text, 'string')

class TestWordsWithModel(unittest.TestCase):
       
    def setUp(self):
        self.model = spacyModel
        
    def assertListSize(self, words, size):
        self.assertEqual(len(words.list), size)
        self.assertEqual(len(words.map), size)
        self.assertEqual(len(words.vectors), size)
            
    def test_empty_words(self):
        words = Words(self.model)
        self.assertEqual(len(words.list), 0)
        self.assertEqual(len(words.map), 0)
               
    def test_add_word(self):
        words = Words(self.model)
        word = Word('test')

        words.add(word)
        self.assertListSize(words, 1)

        words.add(word)
        self.assertListSize(words, 1)
        
        words.add(Word('test2'))
        self.assertListSize(words, 2)
        
        words.clear()
        
        self.assertListSize(words, 0)     

    def test_add_word_string(self):
        words = Words(self.model)
        
        words.add('test')    
        self.assertListSize(words, 1)
        self.assertEqual(words.list[0].text, 'test')
        
        words.clear()
        
        words.add('test test2 test abc')
        self.assertListSize(words, 3)
        self.assertEqual( words.wordWithText('abc').text, 'abc')     
        
        words.clear()
        
        words.add( ['dog', 'cat mouse iceberg', Word('test'), ['dog', Word('test'), 'string']])
        self.assertListSize(words, 6)
        self.assertEqual( words.wordWithText('string').text, 'string')  
        
        words.clear()
        
        words.add('dog cat mouse iceberg')
        
        matches = words.wordsClosestTo('dog')
        self.assertEqual( matches[0][0].text, 'dog')
        
        matches = words.wordsClosestTo('frozen', 0.1)
        self.assertEqual( matches[0][0].text, 'iceberg')
        
        matches = words.wordsClosestTo('rodent', 0.1)
        self.assertEqual( matches[0][0].text, 'mouse')
        
        matches = words.wordsClosestTo('kitty', 0.1)
        self.assertEqual( matches[0][0].text, 'cat')

if __name__ == '__main__':
    unittest.main()
    
