from unittest import TestCase
from toolbox.currency import Currency

class CurrencyTestCase(TestCase):
    def test_equal(self):
        cur1 = Currency(1, 2, 3, 4, 5)
        cur2 = Currency(1, 2, 3, 4, 5)
        self.assertEqual(cur1, cur2)
    
    def test_not_equal_platinum(self):
        cur1 = Currency(1, 2, 3, 4, 5)
        cur2 = Currency(0, 2, 3, 4, 5)
        self.assertNotEqual(cur1, cur2)
    
    def test_not_equal_gold(self):
        cur1 = Currency(1, 2, 3, 4, 5)
        cur2 = Currency(1, 0, 3, 4, 5)
        self.assertNotEqual(cur1, cur2)
    
    def test_not_equal_electrum(self):
        cur1 = Currency(1, 2, 3, 4, 5)
        cur2 = Currency(1, 2, 0, 4, 5)
        self.assertNotEqual(cur1, cur2)
    
    def test_not_equal_silver(self):
        cur1 = Currency(1, 2, 3, 4, 5)
        cur2 = Currency(1, 2, 3, 0, 5)
        self.assertNotEqual(cur1, cur2)
    
    def test_not_equal_copper(self):
        cur1 = Currency(1, 2, 3, 4, 5)
        cur2 = Currency(1, 2, 3, 4, 0)
        self.assertNotEqual(cur1, cur2)
    
    def test_consolidate(self):
        cur1 = Currency(101, 201, 301, 401, 501).consolidate()
        cur2 = Currency(140, 6, 1, 1, 1)
        self.assertEqual(cur1, cur2)
    