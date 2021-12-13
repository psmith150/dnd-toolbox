"""Test the implementation of the dice.py module."""
from unittest import TestCase, main
from toolbox.common import Dice
from toolbox.dice import DieRoll

class DieRollTestCase(TestCase):
    def test_get_min_value_no_modifiers(self):
        roll = DieRoll(Dice.D100)
        self.assertEqual(roll.min_value(), 1)
    
    def test_get_min_value_static_modifiers(self):
        roll = DieRoll(Dice.D100, [10])
        self.assertEqual(roll.min_value(), 11)
    
    def test_get_min_value_dynamic_modifiers(self):
        roll = DieRoll(Dice.D100, [Dice.D4])
        self.assertEqual(roll.min_value(), 2)
    
    def test_get_min_value_mixed_modifiers(self):
        roll = DieRoll(Dice.D100, [Dice.D4, 10])
        self.assertEqual(roll.min_value(), 12)
    