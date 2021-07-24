from __future__ import annotations
from typing import List
from functools import total_ordering
from enum import Flag, auto

class CurrencyOptions(Flag):
    COPPER = 0
    SILVER = auto()
    ELECTRUM = auto()
    GOLD = auto()
    PLATINUM = auto()
    COMMON = COPPER | SILVER | GOLD
    ALL = COPPER | SILVER | ELECTRUM | GOLD | PLATINUM

@total_ordering
class Currency():
    def __init__(self, platinum: int = 0, gold: int = 0, electrum: int = 0, silver: int = 0, copper: int = 0) -> None:
        self.platinum = platinum
        self.gold = gold
        self.electrum = electrum
        self.silver = silver
        self.copper = copper
    
    def __eq__(self, o: object) -> bool:
        if (not isinstance(o,Currency)):
            return False
        equal = self.platinum == o.platinum
        equal &= self.gold == o.gold
        equal &= self.electrum == o.electrum
        equal &= self.silver == o.silver
        equal &= self.copper == o.copper
        return equal
    
    def __lt__(self, o:object) -> bool:
        if (not isinstance(o,Currency)):
            return NotImplemented
        return self.to_copper() < o.to_copper()
    
    def __str__(self) -> str:
        val = ''
        val += f'{self.platinum}pp, ' if self.platinum > 0 else ''
        val += f'{self.gold}gp, ' if self.gold > 0 else ''
        val += f'{self.electrum}ep, ' if self.electrum > 0 else ''
        val += f'{self.silver}sp, ' if self.silver > 0 else ''
        val += f'{self.copper}cp, ' if (self.copper > 0 or self.to_copper() <= 0) else ''
        while (val[-1] == ',' or val[-1] == ' '):
            val = val[:-1]
        return val
    
    def __add__(self, o:object) -> Currency:
        if (not isinstance(o,Currency)):
            return NotImplemented
        return Currency(self.platinum + o.platinum,
                self.gold + o.gold,
                self.electrum + o.electrum,
                self.silver + o.silver,
                self.copper + o.copper)
    
    def __sub__(self, o:object) -> Currency:
        if (not isinstance(o,Currency)):
            return NotImplemented
        result = self.to_copper() - o.to_copper()
        return Currency(copper=result).consolidate(currencies=CurrencyOptions.ALL)
    
    def __mul__(self, o:object) -> Currency:
        if (not (isinstance(o, int) or isinstance(o, float))):
            return NotImplemented
        return Currency(self.platinum * o,
                self.gold * o,
                self.electrum * o,
                self.silver * o,
                self.copper * o)
    
    def to_copper(self) -> int:
        return self.platinum * 1000 + self.gold * 100 + self.electrum * 50 + self.silver * 10 + self.copper
    
    def consolidate(self, currencies: CurrencyOptions=CurrencyOptions.COMMON) -> Currency:
        copper = self.to_copper()
        cur = Currency()
        if (CurrencyOptions.PLATINUM in currencies):
            cur.platinum = copper // 1000
            copper %= 1000
        if (CurrencyOptions.GOLD in currencies):
            cur.gold = copper // 100
            copper %= 100
        if (CurrencyOptions.ELECTRUM in currencies):
            cur.electrum = copper // 50
            copper %= 50
        if (CurrencyOptions.SILVER in currencies):
            cur.silver = copper // 10
            copper %= 10
        cur.copper = copper
        return cur
    
    def split(self, players: int, consolidate: bool=True, consolidate_currencies: CurrencyOptions=CurrencyOptions.COMMON) -> List[Currency]:
        if (consolidate):
            copper = self.to_copper()
            remainder = copper % players
            currencies = []
            for index in range(remainder):
                currencies.append(Currency(copper=copper // players + 1).consolidate(consolidate_currencies))
            for index in range(players - remainder):
                currencies.append(Currency(copper=copper // players).consolidate(consolidate_currencies))
        else:
            coin = self.platinum
            currencies = [Currency() for i in range(players)]
            while (coin > 0):
                min_cur = min(currencies)
                min_cur.platinum += 1
                coin -= 1
            coin = self.gold
            while (coin > 0):
                min_cur = min(currencies)
                min_cur.gold += 1
                coin -= 1
            coin = self.electrum
            while (coin > 0):
                min_cur = min(currencies)
                min_cur.electrum += 1
                coin -= 1
            coin = self.silver
            while (coin > 0):
                min_cur = min(currencies)
                min_cur.silver += 1
                coin -= 1
            coin = self.copper
            while (coin > 0):
                min_cur = min(currencies)
                min_cur.copper += 1
                coin -= 1
        return currencies

        