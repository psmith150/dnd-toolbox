from enum import Enum, auto, IntEnum
from typing import List
from math import floor

class DamageType(Enum):
    BLUDGEONING = auto()
    PIERCING = auto()

class Dice(IntEnum):
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20
    D100 = 100

class Damage:
    def __init__(self, num_dice: int, die: Dice, damage: DamageType) -> None:
        self.num_dice = num_dice
        self.die = die
        self.damage = damage
    
    def average(self) -> float:
        return self.num_dice * (self.die + 1) / 2

class WeaponType(Enum):
    MACE = auto()
    WARHAMMER = auto()

class Weapon:
    _weapon_map = {
        WeaponType.MACE: Damage(1, Dice.D6, DamageType.BLUDGEONING),
        WeaponType.WARHAMMER: Damage(1, Dice.D8, DamageType.BLUDGEONING),
    }
    def __init__(self, weapon_type: WeaponType, bonus: int = 0, extra_damage: List[Damage] = []):
        self.weapon_type = weapon_type
        self.bonus = bonus
        self.extra_damage = extra_damage

    @property
    def base_damage_die(self) -> int:
        return self._weapon_map[self.weapon_type].die

    @property
    def base_damage_type(self):
        return self._weapon_map[self.weapon_type].damage
    
    def average_damage(self):
        average = self._weapon_map[self.weapon_type].average()
        average += self.bonus
        for damage in self.extra_damage:
            average += damage.average()
        return average
    
    def average_critical_damage(self):
        average = 2 * self._weapon_map[self.weapon_type].average()
        average += self.bonus
        for damage in self.extra_damage:
            average += 2 * damage.average()
        return average

class WeaponAttack:
    def __init__(self, weapon: Weapon, level: int, attack_stat: int, proficient: bool = True, damage_mod: int = 0):
        self.weapon = weapon
        self.level = level
        self.attack_stat = attack_stat
        self.proficient = proficient
        self.damage_mod = damage_mod
    
    @property
    def proficiency_bonus(self) -> int:
        if 0 < self.level <= 4:
            return 2
        elif 4 < self.level <= 8:
            return 3
        elif 8 < self.level <= 12:
            return 4
        elif 12 < self.level <= 16:
            return 5
        elif 16 < self.level <= 20:
            return 6
        else:
            return 2
    
    @property
    def attack_mod(self) -> int:
        return floor((self.attack_stat - 10) / 2)
    
    @property
    def hit_bonus(self) -> int:
        return (self.proficiency_bonus if self.proficient else 0) + self.attack_mod
    
    def hit_chance(self, target_ac: int):
        return max(min(Dice.D20 - target_ac + self.hit_bonus + self.weapon.bonus + 1, 19), 1)
    
    def average_hit_damage(self) -> float:
        return self.weapon.average_damage() + self.attack_mod + self.damage_mod
    
    def average_damage(self, target_ac: int) -> float:
        return max((self.hit_chance(target_ac) - 1), 1) / Dice.D20 * self.average_hit_damage() + 1 / Dice.D20 * self.critical_hit_damage()
    
    def critical_hit_damage(self) -> float:
        return self.weapon.average_critical_damage() + self.attack_mod + self.damage_mod