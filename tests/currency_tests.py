from unittest import TestCase, main
from toolbox.currency import Currency, CurrencyOptions

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
    
    def test_to_string(self):
        cur = Currency(1, 2, 3, 4, 5)
        self.assertEqual(str(cur), '1pp, 2gp, 3ep, 4sp, 5cp')
    
    def test_to_string_trailing_commas(self):
        cur = Currency(1, 0, 0, 0, 0)
        self.assertEqual(str(cur), '1pp')
    
    def test_to_string_zero(self):
        cur = Currency(0, 0, 0, 0, 0)
        self.assertEqual(str(cur), '0cp')

    def test_add(self):
        cur1 = Currency(1, 2, 3, 4, 5)
        cur2 = Currency(6, 7, 8, 9, 10)
        self.assertEqual(Currency(7, 9, 11, 13, 15), cur1+cur2)
    
    def test_add_wrong_type(self):
        cur1 = Currency(1, 2, 3, 4, 5)
        self.assertRaises(TypeError, cur1.__add__(1))
    
    def test_sub(self):
        cur1 = Currency(6, 7, 8, 9, 10)
        cur2 = Currency(1, 1, 1, 1, 1)
        self.assertEqual(Currency(5, 6, 7, 8, 9), cur1-cur2)
    
    def test_sub_borrow(self):
        cur1 = Currency(1, 1, 1, 1, 1)
        cur2 = Currency(0, 2, 0, 0, 0)
        self.assertEqual(Currency(0, 9, 1, 1, 1), cur1-cur2)
    
    def test_sub_wrong_type(self):
        cur1 = Currency(1, 2, 3, 4, 5)
        self.assertRaises(TypeError, cur1.__sub__(1))
    
    def test_mul(self):
        cur = Currency(1, 2, 3, 4, 5)
        self.assertEqual(Currency(2, 4, 6, 8, 10), cur * 2)
    
    def test_mul_wrong_type(self):
        cur1 = Currency(1, 2, 3, 4, 5)
        cur2 = Currency(1, 1, 1, 1, 1)
        self.assertRaises(TypeError, cur1.__mul__(cur2))
    
    def test_to_copper(self):
        cur1 = Currency(1, 2, 3, 4, 5)
        self.assertEqual(cur1.to_copper(), 1395)
    
    def test_consolidate_all(self):
        cur1 = Currency(101, 201, 301, 401, 501).consolidate(CurrencyOptions.ALL)
        cur2 = Currency(140, 6, 1, 1, 1)
        self.assertEqual(cur1, cur2)
    
    def test_consolidate_noplatinum(self):
        options = CurrencyOptions.COPPER | CurrencyOptions.SILVER | CurrencyOptions.ELECTRUM | CurrencyOptions.GOLD
        cur1 = Currency(101, 201, 301, 401, 501).consolidate(options)
        cur2 = Currency(0, 1406, 1, 1, 1)
        self.assertEqual(cur1, cur2)
    
    def test_consolidate_nogold(self):
        options = CurrencyOptions.COPPER | CurrencyOptions.SILVER | CurrencyOptions.ELECTRUM | CurrencyOptions.PLATINUM
        cur1 = Currency(101, 201, 301, 401, 501).consolidate(options)
        cur2 = Currency(140, 0, 13, 1, 1)
        self.assertEqual(cur1, cur2)
    
    def test_consolidate_noelectrum(self):
        options = CurrencyOptions.COPPER | CurrencyOptions.SILVER | CurrencyOptions.GOLD | CurrencyOptions.PLATINUM
        cur1 = Currency(101, 201, 301, 401, 501).consolidate(options)
        cur2 = Currency(140, 6, 0, 6, 1)
        self.assertEqual(cur1, cur2)
    
    def test_consolidate_nosilver(self):
        options = CurrencyOptions.COPPER | CurrencyOptions.ELECTRUM | CurrencyOptions.GOLD | CurrencyOptions.PLATINUM
        cur1 = Currency(101, 201, 301, 401, 501).consolidate(options)
        cur2 = Currency(140, 6, 1, 0, 11)
        self.assertEqual(cur1, cur2)
    
    def test_split_evenly_consolidate(self):
        currencies = Currency(100, 100, 100, 100, 100).split(2)
        self.assertEqual(currencies[0], currencies[1])
        self.assertEqual(currencies[0], Currency(gold=580, silver=5))
    
    def test_split_unevenly_consolidate(self):
        currencies = Currency(100, 100, 100, 100, 101).split(2)
        self.assertEqual(currencies[0], Currency(gold=580, silver=5, copper=1))
        self.assertEqual(currencies[1], Currency(gold=580, silver=5))
    
    def test_split_evenly_noconsolidate(self):
        currencies = Currency(100, 100, 100, 100, 100).split(2, False)
        self.assertEqual(currencies[0], currencies[1])
        self.assertEqual(currencies[0], Currency(50, 50, 50, 50, 50))
    
    def test_split_unevenly_noconsolidate(self):
        currencies = Currency(3, 2, 5, 5, 5).split(3, False)
        self.assertEqual(currencies[0], Currency(1, 1, 1, 2, 0))
        self.assertEqual(currencies[1], Currency(1, 1, 1, 2, 0))
        self.assertEqual(currencies[2], Currency(1, 0, 3, 1, 5))