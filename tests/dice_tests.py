"""Test the implementation of the dice.py module."""
from unittest import TestCase, main
from toolbox.common import Dice
from toolbox.dice import DiceRoll, DiceCollection, SpecialRoll

class DiceRollTestCase(TestCase):
    def test_get_min_value_no_modifier(self):
        roll = DiceRoll(Dice.D100, 1)
        self.assertEqual(roll.min_value(), 1)
    
    def test_get_min_value_multiple_dice_no_modifier(self):
        roll = DiceRoll(Dice.D100, 2)
        self.assertEqual(roll.min_value(), 2)
    
    def test_get_min_value_static_modifier(self):
        roll = DiceRoll(Dice.D100, 1, 10)
        self.assertEqual(roll.min_value(), 11)
    
    def test_get_min_value_multiple_dice_static_modifier(self):
        roll = DiceRoll(Dice.D100, 2, 10)
        self.assertEqual(roll.min_value(), 12)
    
    def test_get_min_value_drop_lowest(self):
        roll = DiceRoll(Dice.D100, 2, 0, SpecialRoll.DROP_LOWEST, 1)
        self.assertEqual(roll.min_value(), 1)
    
    def test_get_min_value_drop_highest(self):
        roll = DiceRoll(Dice.D100, 2, 0, SpecialRoll.DROP_HIGHEST, 1)
        self.assertEqual(roll.min_value(), 1)
    
    def test_get_max_value_no_modifier(self):
        roll = DiceRoll(Dice.D100, 1)
        self.assertEqual(roll.max_value(), 100)
    
    def test_get_max_value_multiple_dice_no_modifier(self):
        roll = DiceRoll(Dice.D100, 2)
        self.assertEqual(roll.max_value(), 200)
    
    def test_get_max_value_static_modifier(self):
        roll = DiceRoll(Dice.D100, 1, 10)
        self.assertEqual(roll.max_value(), 110)
    
    def test_get_max_value_multiple_dice_static_modifier(self):
        roll = DiceRoll(Dice.D100, 2, 10)
        self.assertEqual(roll.max_value(), 210)
    
    def test_get_max_value_drop_lowest(self):
        roll = DiceRoll(Dice.D100, 2, 0, SpecialRoll.DROP_LOWEST, 1)
        self.assertEqual(roll.max_value(), 100)
    
    def test_get_max_value_drop_highest(self):
        roll = DiceRoll(Dice.D100, 2, 0, SpecialRoll.DROP_HIGHEST, 1)
        self.assertEqual(roll.max_value(), 100)
    
    def test_get_average_value_no_modifier(self):
        roll = DiceRoll(Dice.D100, 1)
        self.assertAlmostEqual(roll.average_value(), 50.5)
    
    def test_get_average_value_multiple_dice_no_modifier(self):
        roll = DiceRoll(Dice.D100, 2)
        self.assertAlmostEqual(roll.average_value(), 101)
    
    def test_get_average_value_static_modifier(self):
        roll = DiceRoll(Dice.D100, 1, 10)
        self.assertAlmostEqual(roll.average_value(), 60.5)
    
    def test_get_average_value_multiple_dice_static_modifier(self):
        roll = DiceRoll(Dice.D100, 2, 10)
        self.assertAlmostEqual(roll.average_value(), 111)
    
    def test_get_average_value_drop_lowest(self):
        roll = DiceRoll(Dice.D6, 2, 0, SpecialRoll.DROP_LOWEST, 1)
        self.assertAlmostEqual(roll.average_value(), 161/36)
    
    def test_get_average_value_drop_highest(self):
        roll = DiceRoll(Dice.D6, 2, 0, SpecialRoll.DROP_HIGHEST, 1)
        self.assertAlmostEqual(roll.average_value(), 91/36)

    def test_get_all_values_one_die(self):
        roll = DiceRoll(Dice.D6)
        values = roll.get_all_values()
        values.sort()
        self.assertEqual(values.count(1), 1)
        self.assertEqual(values.count(2), 1)
        self.assertEqual(values.count(3), 1)
        self.assertEqual(values.count(4), 1)
        self.assertEqual(values.count(5), 1)
        self.assertEqual(values.count(6), 1)
    
    def test_get_all_values_two_die(self):
        roll = DiceRoll(Dice.D6, 2)
        values = roll.get_all_values()
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

    def test_get_probability_target_single_die(self):
        roll = DiceRoll(Dice.D100, 1)
        self.assertAlmostEqual(roll.get_probability_target(50), 1/100)
    
    def test_get_probability_target_single_die_static_modifier(self):
        roll = DiceRoll(Dice.D100, 1, 1)
        self.assertAlmostEqual(roll.get_probability_target(50), 1/100)
    
    def test_get_probability_target_two_dice(self):
        roll = DiceRoll(Dice.D6, 2)
        self.assertAlmostEqual(roll.get_probability_target(8), 5/36)
    
    def test_get_probability_target_two_dice_and_static_modifier(self):
        roll = DiceRoll(Dice.D6, 2, 1)
        self.assertAlmostEqual(roll.get_probability_target(9), 5/36)
    
    def test_get_probability_target_two_dice_drop_lowest(self):
        roll = DiceRoll(Dice.D100, 2, 0, SpecialRoll.DROP_LOWEST, 1)
        self.assertAlmostEqual(roll.get_probability_target(50), 99/10000)
    
    def test_get_probability_target_two_dice_drop_highest(self):
        roll = DiceRoll(Dice.D100, 2, 0, SpecialRoll.DROP_HIGHEST, 1)
        self.assertAlmostEqual(roll.get_probability_target(50), 101/10000)
    
    def test_get_probability_range_single_die(self):
        roll = DiceRoll(Dice.D100, 1)
        self.assertAlmostEqual(roll.get_probability_range(51, 100), 50/100)
    
    def test_get_probability_range_single_die_static_modifier(self):
        roll = DiceRoll(Dice.D100, 1, 1)
        self.assertAlmostEqual(roll.get_probability_range(51, 100), 50/100)
    
    def test_get_probability_range_two_dice(self):
        roll = DiceRoll(Dice.D6, 2)
        self.assertAlmostEqual(roll.get_probability_range(8, 10), 12/36)
    
    def test_get_probability_range_two_dice_and_static_modifier(self):
        roll = DiceRoll(Dice.D6, 2, 1)
        self.assertAlmostEqual(roll.get_probability_range(8, 10), 15/36)
    
    def test_get_probability_range_two_dice_drop_lowest(self):
        roll = DiceRoll(Dice.D100, 2, 0, SpecialRoll.DROP_LOWEST, 1)
        self.assertAlmostEqual(roll.get_probability_range(49, 51), 297/10000)
    
    def test_get_probability_range_two_dice_drop_highest(self):
        roll = DiceRoll(Dice.D100, 2, 0, SpecialRoll.DROP_HIGHEST, 1)
        self.assertAlmostEqual(roll.get_probability_range(49, 51), 303/10000)
    
    def test_get_all_combinations_single_die(self):
        roll = DiceRoll(Dice.D4, 1)
        combinations = roll.get_all_combinations()
        combinations.sort()
        self.assertEqual(combinations, [[1], [2], [3], [4]])
    
    def test_get_all_combinations_single_die_modifier(self):
        roll = DiceRoll(Dice.D4, 1, 1)
        combinations = roll.get_all_combinations()
        combinations.sort()
        self.assertEqual(combinations, [[1], [2], [3], [4]])
    
    def test_get_all_combinations_two_dice(self):
        roll = DiceRoll(Dice.D4, 2)
        combinations = roll.get_all_combinations()
        combinations.sort()
        self.assertEqual(combinations, [
            [1, 1], [1, 2], [1, 3], [1, 4],
            [2, 1], [2, 2], [2, 3], [2, 4],
            [3, 1], [3, 2], [3, 3], [3, 4],
            [4, 1], [4, 2], [4, 3], [4, 4]])
    
    def test_get_all_combinations_two_dice_modifier(self):
        roll = DiceRoll(Dice.D4, 2, 1)
        combinations = roll.get_all_combinations()
        combinations.sort()
        self.assertEqual(combinations, [
            [1, 1], [1, 2], [1, 3], [1, 4],
            [2, 1], [2, 2], [2, 3], [2, 4],
            [3, 1], [3, 2], [3, 3], [3, 4],
            [4, 1], [4, 2], [4, 3], [4, 4]])

class DiceCollectionTestCase(TestCase):
    def test_get_min_value_no_modifiers(self):
        roll = DiceCollection(Dice.D100)
        self.assertEqual(roll.min_value(), 1)
    
    def test_get_min_value_static_modifiers(self):
        roll = DiceCollection(Dice.D100, [10])
        self.assertEqual(roll.min_value(), 11)
    
    def test_get_min_value_dynamic_modifiers(self):
        roll = DiceCollection(Dice.D100, [Dice.D4])
        self.assertEqual(roll.min_value(), 2)
    
    def test_get_min_value_mixed_modifiers(self):
        roll = DiceCollection(Dice.D100, [Dice.D4, 10])
        self.assertEqual(roll.min_value(), 12)

    def test_get_all_values_one_die(self):
        roll = DiceCollection(Dice.D100)
        values = roll.get_all_values([Dice.D6])
        values.sort()
        self.assertEqual(values.count(1), 1)
        self.assertEqual(values.count(2), 1)
        self.assertEqual(values.count(3), 1)
        self.assertEqual(values.count(4), 1)
        self.assertEqual(values.count(5), 1)
        self.assertEqual(values.count(6), 1)
    
    def test_get_all_values_two_same_die(self):
        roll = DiceCollection(Dice.D100)
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
        roll = DiceCollection(Dice.D100)
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
        roll = DiceCollection(Dice.D100)
        self.assertAlmostEqual(roll.get_probability(50), 1/100)
    
    def test_get_probablility_single_die_static_modifier(self):
        roll = DiceCollection(Dice.D100, [1])
        self.assertAlmostEqual(roll.get_probability(50), 1/100)
    
    def test_get_probability_two_dice(self):
        roll = DiceCollection(Dice.D6, [Dice.D6])
        self.assertAlmostEqual(roll.get_probability(8), 5/36)
    
    def test_get_probability_two_dice_and_static_modifier(self):
        roll = DiceCollection(Dice.D6, [Dice.D6, 1])
        self.assertAlmostEqual(roll.get_probability(9), 5/36)