"""Dice probability calculator

Classes:
    TODO
"""
from __future__ import absolute_import, annotations
import collections
from .common import Dice

class DieRoll():
    """
    Represents a roll of a die.
    """
    def __init__(self, die: Dice, modifiers: list = [], advantage: bool = False) -> None:
        """Initializes the DieRoll object with the given parameters.

        Args:
            die (Dice): The die to use for the base roll
            modifiers (list): Additional modifiers to add to the roll. Defaults to empty.
            advantage (bool, optional): Whether or not to roll with advantage. Defaults to False.
        """
        self.die = die
        self.modifiers = modifiers
        self.advantage = advantage
    
    def min_value(self) -> int:
        base_val = 0 if self.die == Dice.D0 else 1
        mod_val = 0
        for mod in self.modifiers:
            if isinstance(mod, Dice):
                mod_val += 0 if mod == Dice.D0 else 1
            elif isinstance(mod, int):
                mod_val += mod
            else:
                return NotImplemented
        return base_val + mod_val
                

    def max_value(self):
        base_val = self.die.value
        mod_val = 0
        for mod in self.modifiers:
            if isinstance(mod, Dice):
                mod_val += mod.value
            elif isinstance(mod, int):
                mod_val += mod
            else:
                return NotImplemented
        return base_val + mod_val
    
    def get_probability(self, target: int) -> float:
        if target < self.min_value() or target > self.max_value():
            return 0.0
        
        # Subtract all static modifiers
        adjusted_target = target
        for modifier in self.modifiers:
            if (isinstance(modifier, int) and not isinstance(modifier, Dice)):
                adjusted_target -= modifier
        possible_values = []
        dice_modifiers = [mod for mod in self.modifiers if isinstance(mod, Dice)]
        for base_val in range(1, self.die.value + 1):
            possible_values += [base_val + return_val for return_val in self.get_all_values(dice_modifiers)]
        total_possible_outcomes = len(possible_values)
        outcomes = collections.Counter(possible_values)
        target_outcomes = outcomes[adjusted_target]
        return target_outcomes / total_possible_outcomes
    
    def get_all_values(self, dice: list) -> list:
        if len(dice) <= 0:
            return [0]
        if len(dice) == 1:
            return [*range(1, dice[0].value + 1)]
        else:
            values = []
            active_die = dice[0]
            for value in range(1, active_die+1):
                values += [value + return_value for return_value in self.get_all_values(dice[1:])]
            return values

            
    def get_all_probabilities(self) -> dict:
        pass

def calculate(dice: list, target: int) -> float:
    pass