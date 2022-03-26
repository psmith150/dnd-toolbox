from __future__ import annotations
from typing import List
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.sql import select
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class MagicItem():
    """Represents a magical item.
    """
    def __init__(self, name: str, item_type: str, attunement: bool, rarity: str,
                    power_level: str, attunement_requirement: str = '') -> None:
        self.name = name
        self.item_type = item_type
        self.attunement = attunement
        self.rarity = rarity
        self.power_level = power_level
        self.attunement_requirement = attunement_requirement
    
    def __str__(self) -> str:
        return self.name

class MagicItemDbInterface():
    def __init__(self) -> None:
        self.path = 'sqlite:///' + str(Path(__file__).parent / 'data' / 'magic_items.db')
        self.engine = None

    def connect(self) -> bool:
        """Connects to the SQL database.

        Returns:
            bool: If the connection was successful
        """
        self.engine = create_engine(self.path, echo=False)
        return not (self.engine is None)
    
    def is_connected(self) -> bool:
        return not (self.engine is None)
    
    def get_magic_items(self) -> List[MagicItem]:
        if not self.is_connected():
            self.connect()
        if not self.engine:
            logger.error('Unable to connect to database.')
            return []
        else:
            conn = self.engine.connect()
            if not conn:
                logger.error('Unable to connect to database.')
                return []
        meta = MetaData(bind=self.engine)
        items_view = Table('all_items', meta, autoload_with=self.engine)
        statement = select(items_view)
        result = conn.execute(statement)
        rows = result.fetchall()
        items = []
        for row in rows:
            item = MagicItem(row['Name'], row['Type'], bool(row['Attunement']), row['Rarity'], row['PowerLevel'], row['AttunementRequirement'])
            items.append(item)
        return items

class MagicItemDistributionRow():
    def __init__(self, start: int, end: int, common_minor: int = 0, uncommon_minor: int = 0,
                    rare_minor: int = 0, very_rare_minor:int = 0, legendary_minor: int = 0,
                    artifact_minor: int = 0, common_major: int = 0, uncommon_major: int = 0,
                    rare_major: int = 0, very_rare_major:int = 0, legendary_major: int = 0,
                    artifact_major: int = 0) -> None:
        self.start = start if start >= 1 and start <= 20 else 1
        if end >= start:
            if end <= 20:
                self.end = end
            else:
                self.end = 20
        else:
            self.end = self.start
        self.values = {}
        self.values['common_minor'] = max(common_minor, 0)
        self.values['uncommon_minor'] = max(uncommon_minor, 0)
        self.values['rare_minor'] = max(rare_minor, 0)
        self.values['very_rare_minor'] = max(very_rare_minor, 0)
        self.values['legendary_minor'] = max(legendary_minor, 0)
        self.values['artifact_minor'] = max(artifact_minor, 0)
        self.values['common_major'] = max(common_major, 0)
        self.values['uncommon_major'] = max(uncommon_major, 0)
        self.values['rare_major'] = max(rare_major, 0)
        self.values['very_rare_major'] = max(very_rare_major, 0)
        self.values['legendary_major'] = max(legendary_major, 0)
        self.values['artifact_major'] = max(artifact_major, 0)

class MagicItemDistribution():
    def __init__(self) -> None:
        self.rows = []
        self._items = []
    
    def add_item(self, item: MagicItem) -> None:
        self._items.append(item)
    
    def add_items(self, items: List[MagicItem]) -> None:
        for item in items:
            self.add_item(item)
    
    def clear_items(self) -> None:
        self._items = []
    
    def add_row(self, new_row: MagicItemDistributionRow) -> None:
        if any([row for row in self.rows if (row.start <= new_row.start <= row.end) or (row.start <= new_row.end <= row.end)]):
            raise ValueError('Row start and end must not overlap with existing rows.')
        self.rows.append(new_row)
    
    def remove_row(self, row: MagicItemDistributionRow) -> None:
        self.rows.remove(row)
    
    def total_row(self) -> MagicItemDistributionRow:
        total_row = MagicItemDistributionRow(1, 20)
        for row in self.rows:
            for (key, value) in row.values.items():
                total_row.values[key] += value
        return total_row        
    
    def process_items(self, ignore_power_level: bool = False) -> MagicItemDistribution:
        distribution = MagicItemDistribution()
        for row in self.rows:
            new_row = MagicItemDistributionRow(row.start, row.end)
            distribution.add_row(new_row)
        for item in self._items:
            success = False
            for row_index, row in enumerate(distribution.rows):
                try:
                    target = self.rows[row_index].values[self._format_item_key(item)]
                except KeyError:
                    raise NotImplementedError(f'Item classification {item.rarity}/{item.power_level} is undefined.')
                try:
                    actual = distribution.rows[row_index].values[self._format_item_key(item)]
                except KeyError:
                    raise NotImplementedError(f'Item classification {item.rarity}/{item.power_level} is undefined.')
                if actual < target:
                    distribution.rows[row_index].values[self._format_item_key(item)] += 1
                    success = True
                    break
            if not success:
                distribution.rows[-1].values[self._format_item_key(item)] += 1
        return distribution
    
    def _format_item_key(self, item: MagicItem) -> str:
        return f'{item.rarity.replace(" ", "_").lower()}_{item.power_level.replace(" ", "_").lower()}'