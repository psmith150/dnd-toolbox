from enum import Enum, auto, IntEnum
from types import ClassMethodDescriptorType
from typing import List
from math import floor

class DamageType(Enum):
    ACID = auto()
    BLUDGEONING = auto()
    COLD = auto()
    FIRE = auto()
    FORCE = auto()
    LIGHTNING = auto()
    NECROTIC = auto()
    PIERCING = auto()
    POISON = auto()
    PSYCHIC = auto()
    RADIANT = auto()
    SLASHING = auto()
    THUNDER = auto()

    @classmethod
    def get_values(cls):
        values = []
        for name, member in DamageType.__members__.items():
            values.append(name.title())
        return values

    @classmethod
    def get_display_name(cls, value):
        try:
            display = DamageType(value).name.title()
        except ValueError:
            display = 'Unknown'
        return display
    
    @classmethod
    def convert_display_name(cls, name):
        try:
            converted_name = name.upper()
            value = DamageType[converted_name]
        except KeyError:
            value = DamageType.ACID
        return value

class Dice(IntEnum):
    D0 = 0
    D1 = 1
    D2 = 2
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20
    D100 = 100

    @classmethod
    def get_values(cls):
        values = []
        for name, member in Dice.__members__.items():
            values.append(name.lower())
        return values

    @classmethod
    def get_display_name(cls, value):
        try:
            display = Dice(value).name.lower()
        except ValueError:
            display = 'Unknown'
        return display
    
    @classmethod
    def convert_display_name(cls, name):
        try:
            converted_name = name.upper()
            value = Dice[converted_name]
        except KeyError:
            value = Dice.D0
        return value

class Damage:
    def __init__(self, num_dice: int, die: Dice, damage: DamageType) -> None:
        self.num_dice = num_dice
        self.die = die
        self.damage = damage
    
    def average(self) -> float:
        return self.num_dice * (self.die + 1) / 2

class WeaponType(Enum):
    CLUB = auto()
    DAGGER = auto()
    GREATCLUB = auto()
    HANDAXE = auto()
    JAVELIN = auto()
    LIGHT_HAMMER = auto()
    MACE = auto()
    QUARTERSTAFF = auto()
    QUARTERSTAFF2H = auto()
    SICKLE = auto()
    SPEAR = auto()
    LIGHT_CROSSBOW = auto()
    DART = auto()
    SHORTBOW = auto()
    SLING = auto()
    BATTLEAXE = auto()
    BATTLEAXE2H = auto()
    FLAIL = auto()
    GLAIVE = auto()
    GREATAXE = auto()
    GREATSWORD = auto()
    HALBERD = auto()
    LANCE = auto()
    LONGSWORD = auto()
    LONGSWORD2H = auto()
    MAUL = auto()
    MORNINGSTAR = auto()
    PIKE = auto()
    RAPIER = auto()
    SCIMITAR = auto()
    SHORTSWORD = auto()
    TRIDENT = auto()
    TRIDENT2H = auto()
    WAR_PICK = auto()
    WARHAMMER = auto()
    WARHAMMER2H = auto()
    WHIP = auto()
    BLOWGUN = auto()
    HAND_CROSSBOW = auto()
    HEAVY_CROSSBOW = auto()
    LONGBOW = auto()
    NET = auto()

    @classmethod
    def get_values(cls):
        values = []
        for name, member in WeaponType.__members__.items():
            if (name.endswith('2H')):
                values.append(name[:-2].title().replace('_', ' ') + ' (2 hands)')
            else:
                values.append(name.title().replace('_', ' '))
        return values
    
    @classmethod
    def get_display_name(cls, value):
        try:
            name = WeaponType(value).name
            if (name.endswith('2H')):
                name = name[:-2] + ' (2 hands)'
            display = name.title().replace('_', ' ')
        except ValueError:
            display = 'Unknown'
        return display
    
    @classmethod
    def convert_display_name(cls, name):
        try:
            converted_name = name.replace(' (2 hands)', '2H').replace(' ', '_').upper()
            value = WeaponType[converted_name]
        except KeyError:
            value = WeaponType.CLUB
        return value


class Weapon:
    _weapon_map = {
        WeaponType.CLUB: Damage(1, Dice.D4, DamageType.BLUDGEONING),
        WeaponType.DAGGER: Damage(1, Dice.D4, DamageType.PIERCING),
        WeaponType.GREATCLUB: Damage(1, Dice.D8, DamageType.BLUDGEONING),
        WeaponType.HANDAXE: Damage(1, Dice.D6, DamageType.SLASHING),
        WeaponType.JAVELIN: Damage(1, Dice.D6, DamageType.PIERCING),
        WeaponType.LIGHT_HAMMER: Damage(1, Dice.D4, DamageType.BLUDGEONING),
        WeaponType.MACE: Damage(1, Dice.D6, DamageType.BLUDGEONING),
        WeaponType.QUARTERSTAFF: Damage(1, Dice.D6, DamageType.BLUDGEONING),
        WeaponType.QUARTERSTAFF2H: Damage(1, Dice.D8, DamageType.BLUDGEONING),
        WeaponType.SICKLE: Damage(1, Dice.D4, DamageType.SLASHING),
        WeaponType.SPEAR: Damage(1, Dice.D6, DamageType.PIERCING),
        WeaponType.LIGHT_CROSSBOW: Damage(1, Dice.D8, DamageType.PIERCING),
        WeaponType.DART: Damage(1, Dice.D4, DamageType.PIERCING),
        WeaponType.SHORTBOW: Damage(1, Dice.D6, DamageType.PIERCING),
        WeaponType.SLING: Damage(1, Dice.D4, DamageType.BLUDGEONING),
        WeaponType.BATTLEAXE: Damage(1, Dice.D8, DamageType.SLASHING),
        WeaponType.BATTLEAXE2H: Damage(1, Dice.D10, DamageType.SLASHING),
        WeaponType.FLAIL: Damage(1, Dice.D8, DamageType.BLUDGEONING),
        WeaponType.GLAIVE: Damage(1, Dice.D10, DamageType.SLASHING),
        WeaponType.GREATAXE: Damage(1, Dice.D12, DamageType.SLASHING),
        WeaponType.GREATSWORD: Damage(2, Dice.D6, DamageType.SLASHING),
        WeaponType.HALBERD: Damage(1, Dice.D10, DamageType.SLASHING),
        WeaponType.LANCE: Damage(1, Dice.D12, DamageType.PIERCING),
        WeaponType.LONGSWORD: Damage(1, Dice.D8, DamageType.SLASHING),
        WeaponType.LONGSWORD2H: Damage(1, Dice.D10, DamageType.SLASHING),
        WeaponType.MAUL: Damage(2, Dice.D6, DamageType.BLUDGEONING),
        WeaponType.MORNINGSTAR: Damage(1, Dice.D8, DamageType.PIERCING),
        WeaponType.PIKE: Damage(1, Dice.D6, DamageType.PIERCING),
        WeaponType.RAPIER: Damage(1, Dice.D8, DamageType.PIERCING),
        WeaponType.SCIMITAR: Damage(1, Dice.D6, DamageType.SLASHING),
        WeaponType.SHORTSWORD: Damage(1, Dice.D6, DamageType.PIERCING),
        WeaponType.TRIDENT: Damage(1, Dice.D6, DamageType.PIERCING),
        WeaponType.TRIDENT2H: Damage(1, Dice.D8, DamageType.PIERCING),
        WeaponType.WAR_PICK: Damage(1, Dice.D8, DamageType.PIERCING),
        WeaponType.WARHAMMER: Damage(1, Dice.D8, DamageType.BLUDGEONING),
        WeaponType.WARHAMMER2H: Damage(1, Dice.D10, DamageType.BLUDGEONING),
        WeaponType.WHIP: Damage(1, Dice.D4, DamageType.SLASHING),
        WeaponType.BLOWGUN: Damage(1, Dice.D1, DamageType.PIERCING),
        WeaponType.LIGHT_CROSSBOW: Damage(1, Dice.D6, DamageType.PIERCING),
        WeaponType.HEAVY_CROSSBOW: Damage(1, Dice.D10, DamageType.PIERCING),
        WeaponType.LONGBOW: Damage(1, Dice.D8, DamageType.PIERCING),
        WeaponType.NET: Damage(1, Dice.D0, DamageType.SLASHING),
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
        return (self.proficiency_bonus if self.proficient else 0) + self.attack_mod + self.weapon.bonus
    
    def hit_chance(self, target_ac: int):
        return max(min(Dice.D20 - target_ac + self.hit_bonus + 1, 19), 1)
    
    def average_hit_damage(self) -> float:
        return self.weapon.average_damage() + self.attack_mod + self.damage_mod
    
    def average_damage(self, target_ac: int) -> float:
        return max((self.hit_chance(target_ac) - 1), 1) / Dice.D20 * self.average_hit_damage() + 1 / Dice.D20 * self.critical_hit_damage()
    
    def critical_hit_damage(self) -> float:
        return self.weapon.average_critical_damage() + self.attack_mod + self.damage_mod