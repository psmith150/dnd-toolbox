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

    def test_get_all_values_one_die(self):
        roll = DieRoll(Dice.D100)
        values = roll.get_all_values([Dice.D6])
        values.sort()
        self.assertEqual(values.count(1), 1)
        self.assertEqual(values.count(2), 1)
        self.assertEqual(values.count(3), 1)
        self.assertEqual(values.count(4), 1)
        self.assertEqual(values.count(5), 1)
        self.assertEqual(values.count(6), 1)
    
    def test_get_all_values_two_same_die(self):
        roll = DieRoll(Dice.D100)
        values = roll.get_all_values([Dice.D6, Dice.D6])
        values.sort()
        self.assertEqual(values.count(2), 1)
        self.assertEqual(values.count(3), 2)
        self.assertEqual(values.count(4), 3)
        self.assertEqual(values.count(5), 4)
        self.assertEqual(values.count(6), 5)
        self.assertEqual(values.count(7), 6)
        self.assertEqual(values.count(8), 5)
        self.assertEqual(values.count(9), 4)
        self.assertEqual(values.count(10), 3)
        self.assertEqual(values.count(11), 2)
        self.assertEqual(values.count(12), 1)
    
    def test_get_all_values_two_different_die(self):
        roll = DieRoll(Dice.D100)
        values = roll.get_all_values([Dice.D6, Dice.D2])
        values.sort()
        self.assertEqual(values.count(2), 1)
        self.assertEqual(values.count(3), 2)
        self.assertEqual(values.count(4), 2)
        self.assertEqual(values.count(5), 2)
        self.assertEqual(values.count(6), 2)
        self.assertEqual(values.count(7), 2)
        self.assertEqual(values.count(8), 1)

    def test_get_probability_single_die(self):
        roll = DieRoll(Dice.D100)
        self.assertAlmostEqual(roll.get_probability(50), 1/100)
    
    def test_get_probablility_single_die_static_modifier(self):
        roll = DieRoll(Dice.D100, [1])
        self.assertAlmostEqual(roll.get_probability(50), 1/100)
    
    def test_get_probability_two_dice(self):
        roll = DieRoll(Dice.D6, [Dice.D6])
        self.assertAlmostEqual(roll.get_probability(8), 5/36)
    
    def test_get_probability_two_dice_and_static_modifier(self):
        roll = DieRoll(Dice.D6, [Dice.D6, 1])
        self.assertAlmostEqual(roll.get_probability(9), 5/36)