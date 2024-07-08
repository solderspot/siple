import unittest
from test.spacy import spacyModel
from siple import WordGroups, WordGroup

                
class TestWordGroups(unittest.TestCase):
   
    def test_groups(self):
        groups = WordGroups('Actions')
        self.assertEqual(len(groups.list), 0)
        self.assertEqual(len(groups.map), 0)
        
        groups.add('Run')
        self.assertEqual(len(groups.list), 1)
        self.assertEqual(len(groups.map), 1)
        self.assertEqual(groups.list[0].name(), 'run')
        self.assertEqual(groups.map['run'].name(), 'run')
        
        groups.clear()
        self.assertEqual(len(groups.list), 0)
        self.assertEqual(len(groups.map), 0)

        groups.add('run sprint jog jaunt')
        self.assertEqual(len(groups.list), 1)
        self.assertEqual(len(groups.map), 4)
        self.assertEqual(groups.list[0].name(), 'run')
        self.assertEqual(groups.map['jaunt'].name(), 'run')
        
        self.assertIsNone(groups.model())
        groups.setModel(spacyModel)
        self.assertEqual(groups.model(), spacyModel)
        self.assertEqual(groups.list[0].model(), spacyModel)
        
        groups.clear()
        groups.add(['run sprint jog jaunt', 'look spy examine eye'])
        self.assertEqual(len(groups.list), 2)
        self.assertEqual(len(groups.map), 8)
        self.assertEqual(groups.list[1].name(), 'look')
        self.assertEqual(groups.map['eye'].name(), 'look')
        
        with self.assertRaises(ValueError) as context:
            groups.add( 'cook run tickle')
        self.assertEqual(str(context.exception), "word 'run' already assigned to a word group")
        
        group = WordGroup()
        group.words.add('run sprint jog')
        self.assertEqual(group.name(), 'run')
        group.setName('MOVE')
        self.assertEqual(group.name(), 'MOVE')
        group.setName(None)
        self.assertEqual(group.name(), 'run')

if __name__ == '__main__':
    unittest.main()
    
