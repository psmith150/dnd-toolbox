"""Dice probability calculator

Classes:
    TODO
"""
from __future__ import absolute_import, annotations
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
        pass

    def get_all_probabilities(self) -> dict:
        pass

def calculate(dice: list, target: int) -> float:
    pass