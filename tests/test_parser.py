import unittest
from test.spacy import spacyModel
from siple import WordType, Parser

test_data = [
    ('run', [
        ('run', 'verb', [])
    ]),
    ('take all', [
        ('take', 'verb', [
            ('all', 'pron', [])
        ])
    ]),
    ('take everything', [
        ('take', 'verb', [
            ('everything', 'pron', [])
        ])
    ]),
    ('take abc', [
        ('take', 'verb', [
            ('abc', 'unkn', [])
        ])
    ]),
    ('the quick brown fox jumped over the lazy dog', [
        ('jumped', 'verb', [
            ('fox', 'noun', [
                ('brown', 'adjt', []), 
                ('quick', 'adjt', [])                             
            ]),
            ('over', 'prep', [
                ('dog', 'noun', [
                    ('lazy', 'adjt', [])
                ])
            ])
        ]),
    ]),
    ('pick up the shiny sword on the table', [
        ('pick', 'verb', [
            ('sword', 'noun', [
                ('shiny', 'adjt', [])
            ]),
            ('up', 'part', []),            
            ('on', 'prep', [
                ('table', 'noun', [])
            ])
        ])
    ]),
    ('open the ancient chest carefully', [
        ('open', 'verb', [
            ('chest', 'noun', [
                ('ancient', 'adjt', [])
            ]),
            ('carefully', 'advb', [])
        ])
    ]),
    ('read the old map in the dusty library', [
        ('read', 'verb', [
            ('map', 'noun', [
                ('old', 'adjt', [])
            ]),
            ('in', 'prep', [
                ('library', 'noun', [
                    ('dusty', 'adjt', [])
                ]),
            ])
        ])
    ]),
    ('talk to the wise old man in the village', [
        ('talk', 'verb', [
            ('to', 'prep', [
                ('man', 'noun', [
                    ('wise', 'adjt', []),
                    ('old', 'adjt', [])
                ])
            ]),
            ('in', 'prep', [
                ('village', 'noun', [])
            ])
        ])
    ]),
    ('unlock the heavy iron gate with the golden key', [
        ('unlock', 'verb', [
            ('gate', 'noun', [
                ('iron', 'adjt', []),
                ('heavy', 'adjt', [])
            ]),
            ('with', 'prep', [
                ('key', 'noun', [
                    ('golden', 'adjt', [])
                ])
            ])
        ])
    ]),
    ('climb up the tall oak tree quickly', [
        ('climb', 'verb', [
            ('tree', 'noun', [
                ('oak', 'adjt', []),
                ('tall', 'adjt', [])
            ]),
            ('up', 'part', []),
            ('quickly', 'advb', [])
        ])
    ]),
    ('search the dark cave for hidden treasures', [
        ('search', 'verb', [
            ('cave', 'noun', [
                ('dark', 'adjt', [])
            ]),
            ('for', 'prep', [
                ('treasures', 'noun', [
                    ('hidden', 'adjt', [])
                ])
            ])
        ])
    ]),
    ('light the old lantern in the damp cellar', [
        ('light', 'verb', [
            ('lantern', 'noun', [
                ('old', 'adjt', [])
            ]),
            ('in', 'prep', [
                ('cellar', 'noun', [
                    ('damp', 'adjt', [])
                ])
            ])
        ])
    ]),
    ('move the large rock aside', [
        ('move', 'verb', [
            ('rock', 'noun', [
                ('large', 'adjt', [])
            ]),
            ('aside', 'advb', []),
        ])
    ]),
    ('look carefully under the bed', [
        ('look', 'verb', [
            ('carefully', 'advb', []),
            ('under', 'prep', [
                ('bed', 'noun', [])
            ])
        ])
    ]),
    ('give the old book to the librarian', [
        ('give', 'verb', [
            ('book', 'noun', [
                ('old', 'adjt', [])
            ]),
            ('to', 'prep', [
                ('librarian', 'noun', [])
            ])
        ])
    ]),
    ('enter the haunted mansion at midnight', [
        ('enter', 'verb', [
            ('mansion', 'noun', [
                ('haunted', 'adjt', [])
            ]),
            ('at', 'prep', [
                ('midnight', 'noun', [])
            ])
        ])
    ]),
    ('cross the rickety bridge over the raging river', [
        ('cross', 'verb', [
            ('bridge', 'noun', [
                ('rickety', 'adjt', [])
            ]),
            ('over', 'prep', [
                ('river', 'noun', [
                    ('raging', 'adjt', [])
                ])
            ])
        ])
    ]),
    ('drink the potion from the green flask', [
        ('drink', 'verb', [
            ('potion', 'noun', []),
            ('from', 'prep', [
                ('flask', 'noun', [
                    ('green', 'adjt', [])
                ])
            ])            
        ])
    ]),
    ('attack the goblin with the rusty sword', [
        ('attack', 'verb', [
            ('goblin', 'noun', []),
            ('with', 'prep', [
                ('sword', 'noun', [
                    ('rusty', 'adjt', [])
                ])
            ])
        ])
    ]),
    ('find the hidden key in the garden', [
        ('find', 'verb', [
            ('key', 'noun', [
                ('hidden', 'adjt', [])
            ]),
            ('in', 'prep', [
                ('garden', 'noun', [])
            ])
        ])
    ]),
    ('read the letter from the mysterious stranger', [
        ('read', 'verb', [
            ('letter', 'noun', []),
            ('from', 'prep', [
                ('stranger', 'noun', [
                    ('mysterious', 'adjt', [])
                ])
            ])
        ])
    ]),
    ('escape the burning building through the window', [
        ('escape', 'verb', [
            ('building', 'noun', [
                ('burning', 'adjt', [])
            ]),
            ('through', 'prep', [
                ('window', 'noun', [])
            ])
        ])
    ]),
    ('throw the longest rope to the person in the pit', [
        ('throw', 'verb', [
            ('rope', 'noun', [
                ('longest', 'adjt', [])
            ]),
            ('to', 'prep', [
                ('person', 'noun', [])
            ]),
            ('in', 'prep', [
                ('pit', 'noun', [])
            ])
        ])
    ]),
    ('whisper the secret code to the guard', [
        ('whisper', 'verb', [
            ('code', 'noun', [
                ('secret', 'adjt', [])
            ]),
            ('to', 'prep', [
                ('guard', 'noun', [])
            ])
        ])
    ]),
    ('navigate the ship through the stormy sea', [
        ('navigate', 'verb', [
            ('ship', 'noun', []),
            ('through', 'prep', [
                ('sea', 'noun', [
                    ('stormy', 'adjt', [])
                ])
            ])
        ])
    ]),
    ('unlock the secret door with the ancient key', [
        ('unlock', 'verb', [
            ('door', 'noun', [
                ('secret', 'adjt', [])
            ]),
            ('with', 'prep', [
                ('key', 'noun', [
                    ('ancient', 'adjt', [])
                ])
            ])
        ])
    ]),
    ('rescue the princess from the tall tower', [
        ('rescue', 'verb', [
            ('princess', 'noun', []),
            ('from', 'prep', [
                ('tower', 'noun', [
                    ('tall', 'adjt', [])
                ])
            ])
        ])
    ]),
    # ('use the magic wand with book to cast a spell', [
    #     ('use', 'verb', [
    #         ('wand', 'noun', [
    #             ('magic', 'adjt', [])
    #         ]),
    #         ('to', 'prep', [
    #             ('cast', 'verb', [
    #                 ('spell', 'noun', [])
    #             ])
    #         ])
    #     ])
    # ]),
    ('hide the treasure in the cave behind the waterfall', [
        ('hide', 'verb', [
            ('treasure', 'noun', []),
            ('in', 'prep', [
                ('cave', 'noun', [])
            ]),
            ('behind', 'prep', [
                ('waterfall', 'noun', [])
            ])
        ])
    ]),
    ('climb the mountain', [
        ('climb', 'verb', [
            ('mountain', 'noun', [])
        ])
    ]),
    ('strike the enemy with the enchanted sword', [
        ('strike', 'verb', [
            ('enemy', 'noun', []),
            ('with', 'prep', [
                ('sword', 'noun', [
                    ('enchanted', 'adjt', [])
                ])
            ])
        ])
    ]),
    # ('strike the enemy with the enchanted sword and the invisible arrow', [
    #     ('strike', 'verb', [
    #         ('enemy', 'noun', []),
    #         ('with', 'prep', [
    #             ('sword', 'noun', [
    #                 ('enchanted', 'adjt', [])
    #             ]),
    #             ('arrow', 'noun', [
    #                 ('invisible', 'adjt', [])
    #             ])
    #         ])
    #     ])
    # ]),
    ('follow the path through the dense forest', [
        ('follow', 'verb', [
            ('path', 'noun', []),
            ('through', 'prep', [
                ('forest', 'noun', [
                    ('dense', 'adjt', [])
                ])
            ])
        ])
    ])
]

                
class TestParser(unittest.TestCase):
    
    def setUp(self) -> None:
        super().setUp()
        self.parser = Parser(spacyModel)
   
    def test_simple(self):
        verbs = self.parser.parse('run')
        self.assertEqual(len(verbs), 1)
        word = verbs[0]
        self.assertEqual(word.text, 'run')
        self.assertEqual(word.type, WordType.VERB)
        
    def find_word(self, text, type, list):
        for word in list:
            if word.text == text and word.type == type:
                return word
        return None
        
    def assert_expected(self, text, type, children, words) -> str:
        word = self.find_word(text, WordType.from_string(type), words)
        if word is None:
            return f"Word {text} of type {type} not found in {words}"
        for child_text, child_type, child_children in children:
            result = self.assert_expected(child_text, child_type, child_children, word.childern)
            if result:
                return result

    def test_parser(self):
        for sentence, expected in test_data:
            words = self.parser.parse(sentence)
            for text, type, children in expected:
                result = self.assert_expected(text, type, children, words)
                if result:
                    word = self.find_word(text, WordType.from_string(type), words)
                    print(sentence)
                    if word:
                        word.printTree()
                    self.fail(result)
        

if __name__ == '__main__':
    unittest.main()
    
