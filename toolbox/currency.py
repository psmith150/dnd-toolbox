from __future__ import annotations
from typing import List

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
    
    def consolidate(self, noplatinum: bool=True, nogold: bool=False, noelectrum: bool=True, nosilver: bool=False) -> Currency:
        cur = Currency()
        cur.silver = self.silver + self.copper // 10
        cur.copper = self.copper % 10
        cur.electrum = self.electrum + cur.silver // 5
        cur.silver = cur.silver % 5
        cur.gold = self.gold + cur.electrum // 2
        cur.electrum = cur.electrum % 2
        cur.platinum = self.platinum + cur.gold // 10
        cur.gold = cur.gold % 10

        return cur
    
    def split(self, players: int, consolidate: bool=True) -> List[Currency]:
        if (consolidate):
            copper = self.platinum * 1000 + self.gold * 100 + self.electrum * 50 + self.silver * 10 + self.copper
            remainder = copper % players
            currencies = []
            for index in range(remainder):
                currencies.append(Currency(copper=copper // players + 1).consolidate())
            for index in range(players - remainder):
                currencies.append(Currency(copper=copper // players).consolidate())
        else:
            currencies = []
        return currencies

        