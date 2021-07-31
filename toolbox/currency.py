"""Represent currency in Dungeons & Dragons 5th edition and allow for operations with currency.

Classes:
    CurrencyOptions
    Currency
"""
from __future__ import annotations, absolute_import
from typing import List
from functools import total_ordering
from enum import Flag, auto

class CurrencyOptions(Flag):
    """Defines an enumeration of damage types.
    
    Members:
        COPPER
        SILVER
        ELECTRUM
        GOLD
        PLATINUM
        COMMON
        ALL
    """
    COPPER = 0
    SILVER = auto()
    ELECTRUM = auto()
    GOLD = auto()
    PLATINUM = auto()
    COMMON = COPPER | SILVER | GOLD
    ALL = COPPER | SILVER | ELECTRUM | GOLD | PLATINUM

@total_ordering
class Currency():
    """Represents a collection of the 5 types of coins.

    Allows comparison, addition, subtraction, and multiplication.
    
    Methods:
        to_copper: Return the number of copper coins equivalent to the total value.
        consolidate: Consolidate the coins into the fewest number possible.
        split: Split the currency into a given number of groups as equally as possible.
        """
    def __init__(self, platinum: int = 0, gold: int = 0, electrum: int = 0, silver: int = 0,
                 copper: int = 0) -> None:
        """Initializes the Currency object with the given coin values.

        Args:
            platinum (int, optional): The number of platinum coins. Defaults to 0.
            gold (int, optional): The number of gold coins. Defaults to 0.
            electrum (int, optional): The number of electrum coins. Defaults to 0.
            silver (int, optional): The number of silver coins. Defaults to 0.
            copper (int, optional): The number of copper coins. Defaults to 0.
        """
        self.platinum = platinum
        self.gold = gold
        self.electrum = electrum
        self.silver = silver
        self.copper = copper
    
    def __eq__(self, other: object) -> bool:
        """Checks for equality between two Currency objects

        Args:
            other (object): The Currency object to compare to

        Returns:
            bool: True if the objects have equal amounts of each coin.
        """
        if not isinstance(other, Currency):
            return False
        equal = self.platinum == other.platinum
        equal &= self.gold == other.gold
        equal &= self.electrum == other.electrum
        equal &= self.silver == other.silver
        equal &= self.copper == other.copper
        return equal
    
    def __lt__(self, other: object) -> bool:
        """Checks if a Currency object is less than the other.

        Args:
            other (object): The Currency object to compare with.

        Returns:
            bool: True if the object's overall value is less.
        """
        if not isinstance(other, Currency):
            return NotImplemented
        return self.to_copper() < other.to_copper()
    
    def __str__(self) -> str:
        """Converts the object to a string representation.

        Object is represented by displaying the number of coins.

        Returns:
            str: The string representation.
        """
        val = ''
        val += f'{self.platinum}pp, ' if self.platinum > 0 else ''
        val += f'{self.gold}gp, ' if self.gold > 0 else ''
        val += f'{self.electrum}ep, ' if self.electrum > 0 else ''
        val += f'{self.silver}sp, ' if self.silver > 0 else ''
        val += f'{self.copper}cp, ' if (self.copper > 0 or self.to_copper() <= 0) else ''
        while (val[-1] == ',' or val[-1] == ' '):
            val = val[:-1]
        return val
    
    def __add__(self, other: object) -> Currency:
        """Adds the Currency object to another Currency object.

        Args:
            other (object): The Currency object to add.

        Returns:
            Currency: A Currency object with the sum of the numbers of coins.
        """
        if not isinstance(other, Currency):
            return NotImplemented
        return Currency(self.platinum + other.platinum,
                        self.gold + other.gold,
                        self.electrum + other.electrum,
                        self.silver + other.silver,
                        self.copper + other.copper)
    
    def __sub__(self, other: object) -> Currency:
        """Subtracts the Currency object from the current object.

        Args:
            other (object): The Currency object to subtract.

        Returns:
            Currency: A Currency object created by subtracting the overall values and
            consolidating.
        """
        if not isinstance(other, Currency):
            return NotImplemented
        result = self.to_copper() - other.to_copper()
        return Currency(copper=result).consolidate(currencies=CurrencyOptions.ALL)
    
    def __mul__(self, other: object) -> Currency:
        """Multiplies the Currency object by a number.

        Args:
            other (object): A float or int to multiply by.

        Returns:
            Currency: A Currency object obtained by multiplying each number of coins by the value.
        """
        if not isinstance(other, (int, float)):
            return NotImplemented
        return Currency(self.platinum * other,
                        self.gold * other,
                        self.electrum * other,
                        self.silver * other,
                        self.copper * other)
    
    def to_copper(self) -> int:
        """Return the equivalent value of the object in copper coins.

        Returns:
            int: The number of copper coins.
        """
        return (self.platinum * 1000 + self.gold * 100 + self.electrum * 50
                + self.silver * 10 + self.copper)
    
    def consolidate(self, currencies: CurrencyOptions = CurrencyOptions.COMMON) -> Currency:
        """Return a Currency object that has been consolidated into the fewest number of coins.

        The types of coins used when consolidating can be specified.

        Args:
            currencies (CurrencyOptions, optional): The coins to use when consolidating.
                Defaults to CurrencyOptions.COMMON.

        Returns:
            Currency: A Currency object with the consolidated values of coins.
        """
        copper = self.to_copper()
        cur = Currency()
        if CurrencyOptions.PLATINUM in currencies:
            cur.platinum = copper // 1000
            copper %= 1000
        if CurrencyOptions.GOLD in currencies:
            cur.gold = copper // 100
            copper %= 100
        if CurrencyOptions.ELECTRUM in currencies:
            cur.electrum = copper // 50
            copper %= 50
        if CurrencyOptions.SILVER in currencies:
            cur.silver = copper // 10
            copper %= 10
        cur.copper = copper
        return cur
    
    def split(self, players: int, consolidate: bool = True,
              consolidate_currencies: CurrencyOptions = CurrencyOptions.COMMON) -> List[Currency]:
        """Return a list of Currency objects obtained by splitting the Currency as
           evenly as possible.

        The returned object can optionally be consolidated into the desired coins.

        Args:
            players (int): The number of players to split the Currency among.
            consolidate (bool, optional): If True, the resulting Currency object will be
                consolidated, as if with the Currency.consolidate() method. Defaults to True.
            consolidate_currencies (CurrencyOptions, optional): The coins to use when
                consolidating. Has no effect if consolidated is False. Defaults to
                CurrencyOptions.COMMON.

        Returns:
            List[Currency]: [description]
        """
        if consolidate:
            copper = self.to_copper()
            remainder = copper % players
            currencies = []
            for _ in range(remainder):
                currencies.append(Currency(copper=copper // players + 1)
                                  .consolidate(consolidate_currencies))
            for _ in range(players - remainder):
                currencies.append(Currency(copper=copper // players)
                                  .consolidate(consolidate_currencies))
        else:
            coin = self.platinum
            currencies = [Currency() for i in range(players)]
            while coin > 0:
                min_cur = min(currencies)
                min_cur.platinum += 1
                coin -= 1
            coin = self.gold
            while coin > 0:
                min_cur = min(currencies)
                min_cur.gold += 1
                coin -= 1
            coin = self.electrum
            while coin > 0:
                min_cur = min(currencies)
                min_cur.electrum += 1
                coin -= 1
            coin = self.silver
            while coin > 0:
                min_cur = min(currencies)
                min_cur.silver += 1
                coin -= 1
            coin = self.copper
            while coin > 0:
                min_cur = min(currencies)
                min_cur.copper += 1
                coin -= 1
        return currencies