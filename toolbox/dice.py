"""Dice probability calculator

Classes:
    TODO
"""
from __future__ import absolute_import, annotations
import collections
from enum import Enum, auto
from .common import Dice
from math import ceil

class SpecialRoll(Enum):
    NONE = auto()
    DROP_LOWEST = auto()
    DROP_HIGHEST = auto()
    # TODO REPLACE_LOWER = auto()
    # TODO REPLACE_HIGHER = auto()

class DiceRoll():
    """Represents a roll of a number of same-sided dice.
    """
    def __init__(self, die: Dice, number: int = 1, modifier: int = 0,
        special: SpecialRoll = SpecialRoll.NONE, special_value: int = 0) -> None:
        """Initializes the DiceRoll object with the given parameters.

        Args:
            die (Dice): The die to use for the base roll
            number (int, optional): The number of dice to roll. Defaults to 1.
            modifier (int, optional): An additional modifier to add to the roll. Defaults to 0.
            special (SpecialRoll, optional): Special modifiers to the roll. Defaults to NONE.
            special_value (int, optional): The value to apply to the selected special. Defaults to 0.
        """
        self.die = die
        self.number = int(number) if int(number) > 0 else 1
        self.modifier = int(modifier)
        self.special = special
        if special_value >= number:
            self.special_value = number - 1
        elif special_value < 0:
            self.special_value = 0
        else:
            self.special_value = special_value
    
    def min_value(self) -> int:
        """Calculates the minimum possible value of the dice roll.

        Returns:
            int: The mimimum possible value of the dice roll.
        """
        base_val = 0 if self.die == Dice.D0 else 1
        if (self.special == SpecialRoll.NONE):
            return base_val * self.number + self.modifier 
        elif (self.special == SpecialRoll.DROP_LOWEST):
            return base_val * (self.number - self.special_value) + self.modifier  
        elif (self.special == SpecialRoll.DROP_HIGHEST):
            return base_val * (self.number - self.special_value) + self.modifier 
        else:
            return NotImplemented 

    def max_value(self):
        """Calculates the maximum possible value of the dice roll.

        Returns:
            int: The maximum possible value of the dice roll.
        """
        if (self.special == SpecialRoll.NONE):
            return self.die.value * self.number + self.modifier 
        elif (self.special == SpecialRoll.DROP_LOWEST):
            return self.die.value * (self.number - self.special_value) + self.modifier  
        elif (self.special == SpecialRoll.DROP_HIGHEST):
            return self.die.value * (self.number - self.special_value) + self.modifier 
        else:
            return NotImplemented 
    
    def average_value(self) -> float:
        """Calculates the average value of the dice roll.

        Returns:
            float: The average value of the dice roll.
        """
        values = self.get_all_values()
        values = [v + self.modifier for v in values]
        return sum(values) / len(values)
    
    def get_probability_target(self, target: int) -> float:
        """Calculates the probability of the dice roll totaling a given value.

        Args:
            target (int): The target value.

        Returns:
            float: The probability of totaling the target value.
        """
        if target < self.min_value() or target > self.max_value():
            return 0.0
        probabilities = self.get_all_probabilities()
        return probabilities[target]
    
    def get_probability_range(self, min_value: int, max_value: int) -> float:
        """Calculates the probability of the dice roll landing within a given range.

        Args:
            min_value (int): The minimum value of the range (inclusive).
            max_value (int): The maximum value of the range (exclusive).

        Returns:
            float: The probability of the total roll being within the range.
        """
        if min_value < self.min_value() or max_value > self.max_value() or min_value > max_value:
            return 0.0
        probabilities = self.get_all_probabilities()
        return sum([probabilities[p] for p in probabilities.keys() if min_value <= p <= max_value])
    
    def get_all_probabilities(self) -> dict[int, float]:
        """Calculates the probability of rolling each possible value.

        Returns:
            dict[int, float]: A dictionary where they keys are possible die rolls and the values are the probability of the roll.
        """
        possible_values = self.get_all_values()
        possible_values = [v + self.modifier for v in possible_values]
        total_possible_outcomes = len(possible_values)
        outcomes = collections.Counter(possible_values)
        return {p:outcomes[p] / total_possible_outcomes for p in range(self.min_value(), self.max_value() + 1)}
    
    def get_all_values(self) -> list[int]:
        """Gets all possible values of the dice roll, not considering the modifier.
        List of all values will include all duplicates.

        Returns:
            list[int]: A list of all possible dice rolls.
        """
        combinations = self.get_all_combinations()
        values = []
        for combination in combinations:
            values.append(sum(combination))
        return values
        #return self.get_values(self.number)

    # def get_values(self, number: int) -> list:
    #     if number <= 0:
    #         return [0]
    #     if number == 1:
    #         return [v for v in range(1, self.die.value + 1)]
    #     else:
    #         values = []
    #         for value in range(1, self.die.value + 1):
    #             values += [value + return_value for return_value in self.get_values(number - 1)]
    #         return values
    
    def get_all_combinations(self) -> list[list[int]]:
        """Gets all possible combinations of the dice, not considering the modifier.

        Returns:
            list[list[int]]: A list of lists of dice values.
        """
        combinations = self._get_combinations(self.number)
        if (self.special == SpecialRoll.NONE):
            pass
        elif (self.special == SpecialRoll.DROP_HIGHEST):
            for combination in combinations:
                for _ in range(self.special_value):
                    combination.remove(max(combination))
        elif (self.special == SpecialRoll.DROP_LOWEST):
            for combination in combinations:
                for _ in range(self.special_value):
                    combination.remove(min(combination))
        else:
            return NotImplemented
        return combinations

    def _get_combinations(self, number: int) -> list[list[int]]:
        """Gets all possible combinations of the specified number of dice, not considering the modifier.

        Args:
            number (int): The number of dice to get combinations for.

        Returns:
            list[list[int]]: A list of lists of dice values.
        """
        if number <= 0:
            return [0]
        if number == 1:
            return [[v] for v in range(1, self.die.value + 1)]
        else:
            if self.die == Dice.D0:
                return [0]
            values = []
            for value in range(1, self.die.value + 1):
                for combination in self._get_combinations(number - 1):
                    values.append([value] + combination)
            return values

class DiceCollection():
    """
    Represents a collection of DiceRoll objects.
    """
    def __init__(self, dice: list[DiceRoll], special: SpecialRoll = SpecialRoll.NONE,
        special_value: int = 0) -> None:
        """Initializes the DiceCollection object with the given parameters.

        Args:
            dice (list[DiceRoll]): The DiceRolls to use in the collection.
            special (SpecialRoll, optional): Special modifiers to the roll collection. Defaults to NONE.
            special_value (int, optional): The value to apply to the selected special. Defaults to 0.
        """
        self.dice = dice
        self.special = special
        self.special_value = special_value
    
    def min_value(self) -> int:
        """Calculates the minimum possible value of the dice rolls.

        Returns:
            int: The minimum possible value of the dice rolls.
        """
        values = [d.min_value() for d in self.dice]
        if (self.special == SpecialRoll.NONE):
            return sum(values)
        elif (self.special == SpecialRoll.DROP_LOWEST):
            for _ in range(self.special_value):
                values.remove(min(values))
            return sum(values)
        elif (self.special == SpecialRoll.DROP_HIGHEST):
            for _ in range(self.special_value):
                values.remove(max(values))
            return sum(values)
        else:
            return NotImplemented               

    def max_value(self) -> int:
        """Calculates the maximum possible value of the dice rolls.

        Returns:
            int: The maximum possible value of the dice rolls.
        """
        values = [d.max_value() for d in self.dice]
        if (self.special == SpecialRoll.NONE):
            return sum(values)
        elif (self.special == SpecialRoll.DROP_LOWEST):
            for _ in range(self.special_value):
                values.remove(min(values))
            return sum(values)
        elif (self.special == SpecialRoll.DROP_HIGHEST):
            for _ in range(self.special_value):
                values.remove(max(values))
            return sum(values)
        else:
            return NotImplemented 
    
    def get_probability_target(self, target: int) -> float:
        """Calculates the probability of the dice rolls totaling a given value.

        Args:
            target (int): The target value.

        Returns:
            float: The probability of totaling the target value.
        """
        if target < self.min_value() or target > self.max_value():
            return 0.0
        probabilities = self.get_all_probabilities()
        return probabilities[target]
    
    def get_probability_range(self, min_value: int, max_value: int) -> float:
        """Calculates the probability of the dice roll landing within a given range.

        Args:
            min_value (int): The minimum value of the range (inclusive).
            max_value (int): The maximum value of the range (exclusive).

        Returns:
            float: The probability of the total roll being within the range.
        """
        if min_value < self.min_value() or max_value > self.max_value() or min_value > max_value:
            return 0.0
        probabilities = self.get_all_probabilities()
        return sum([probabilities[p] for p in probabilities.keys() if min_value <= p <= max_value])
    
    def get_all_probabilities(self) -> dict[int, float]:
        """Calculates the probability of rolling each possible value.

        Returns:
            dict[int, float]: A dictionary where they keys are possible die rolls and the values are the probability of the roll.
        """
        possible_values = self.get_all_values()
        possible_values = [v + self.modifier for v in possible_values]
        total_possible_outcomes = len(possible_values)
        outcomes = collections.Counter(possible_values)
        return {p:outcomes[p] / total_possible_outcomes for p in range(self.min_value(), self.max_value() + 1)}
    
    def get_all_values(self) -> list[int]:
        """Gets all possible values of the dice rolls.

        Returns:
            list[int]: A list of all possible dice rolls.
        """
        combinations = self.get_all_combinations()
        values = []
        for combination in combinations:
            values.append(sum(combination))
        return values
    
    def get_all_combinations(self) -> list[list[int]]:
        """Gets all possible combinations of the dice.

        Returns:
            list[list[int]]: A list of lists of dice values.
        """
        combinations = self._get_combinations(self.dice)
        if (self.special == SpecialRoll.NONE):
            pass
        elif (self.special == SpecialRoll.DROP_HIGHEST):
            for combination in combinations:
                for _ in range(self.special_value):
                    combination.remove(max(combination))
        elif (self.special == SpecialRoll.DROP_LOWEST):
            for combination in combinations:
                for _ in range(self.special_value):
                    combination.remove(min(combination))
        else:
            return NotImplemented
        return combinations

    def _get_combinations(self, dice: list[DiceRoll]) -> list[list[int]]:
        """Gets all possible combinations of the specified dice.

        Args:
            dice (list[DiceRoll]): The DiceRolls to calculate combinations for.

        Returns:
            list[list[int]]: A list of lists of dice values.
        """
        if len(dice) <= 0:
            return [0]
        if len(dice) == 1:
            return [[v] for v in dice[0].get_all_values()]
        else:
            values = []
            current_dice = dice[0]
            for value in current_dice.get_all_values():
                for combination in self._get_combinations(dice[1:]):
                    values.append([value] + combination)
            return values