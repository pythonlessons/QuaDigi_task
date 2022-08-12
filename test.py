import unittest
from main import ForestCounter

class TestForestCounter(unittest.TestCase):

    def test_forest(self):
        forestMap = [
            '0X0X0',
            '00XX0',
            '00000', 
            '0XX00', 
        ]

        forest = ForestCounter(forestMap)
        self.assertEqual(forest.get_forests(), 2)

    def test_large_forest(self):
        forestMap = [
            '0X0X00X0X0',
            '00XX0X0XX0',
            'X000000X00', 
            '0XX000XX00',
            '0000X00000',
            '0000XXXX00', 
        ]

        forest = ForestCounter(forestMap)
        self.assertEqual(forest.get_forests(), 4)

    def test_bad_forest_shape(self):
        forestMap = [
            '0X0X0',
            '00XX0',
            '0000', 
            '0XX', 
        ]

        forest = ForestCounter(forestMap)
        self.assertEqual(forest.get_forests(), 2)


    def test_bad_forest_syntax(self):
        forestMap = [
            '0X0X0',
            '00XX0',
            '00000', 
            '0XX0Z', 
        ]

        with self.assertRaises(Exception):
            ForestCounter(forestMap)

if __name__ == '__main__':
    unittest.main()