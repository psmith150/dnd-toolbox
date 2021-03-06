"""Perform calculations related to combat in Dungeons & Dragons 5th edition.

Classes:

    DamageType: Enumeration of different damage types.
    Dice: Enumeration of different dice types.
    Damage: Represents a damage calculation.
    WeaponType: Enumeration of different weapon types.
    Weapon: Represents a weapon used to make an attack.
    WeaponAttack: Represents an attack made by a weapon.
"""
from __future__ import division, absolute_import
from enum import Enum, auto, IntEnum
from typing import List
from math import floor

class DamageType(Enum):
    """Defines an enumeration of damage types.
    
    Members:
        ACID
        BLUDGEONING
        COLD
        FIRE
        FORCE
        LIGHTNING
        NECROTIC
        PIERCING
        POISON
        PSYCHIC
        RADIANT
        SLASHING
        THUNDER
    
    Methods:
        get_values: Return a list of string representations of the members.
        get_display_name: Get a formatted string representation of a member.
        convert_display_name: Convert a string representation of a member into the member object.
    """

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
    def get_values(cls) -> List[str]:
        """Return a list of string representations of the class' members.
        
        Returns:
            A list of string representations of the class' members.
        """
        values = []
        for name, _ in DamageType.__members__.items():
            values.append(name.title())
        return values

    @classmethod
    def get_display_name(cls, value):
        """Return a string representation of a member.

        Members are represented by the member name in titlecase.
        
        Args:
            value:
                A member of the class.
        
        Returns:
            A string representing the member.
        """
        try:
            display = DamageType(value).name.title()
        except ValueError:
            display = 'Unknown'
        return display
    
    @classmethod
    def convert_display_name(cls, name):
        """Convert a string name into the corresponding class name.

        Strings are converted by transforming the string into uppercase
        and matching the result against all members.
        
        Args:
            name:
                The name to convert.
        
        Returns:
            The matching member.
        """
        try:
            converted_name = name.upper()
            value = DamageType[converted_name]
        except KeyError:
            value = DamageType.ACID
        return value

class Dice(IntEnum):
    """Defines an enumeration of dice types.
    
    Members:
        D0
        D1
        D2
        D4
        D6
        D8
        D10
        D12
        D20
        D100
    
    Methods:
        get_values: Return a list of string representations of the members.
        get_display_name: Get a formatted string representation of a member.
        convert_display_name: Convert a string representatino of a member into the member object.
    """
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
        """Return a list of string representations of the class' members.
        
        Returns:
            A list of string representations of the class' members.
        """
        values = []
        for name, _ in Dice.__members__.items():
            values.append(name.lower())
        return values

    @classmethod
    def get_display_name(cls, value):
        """Return a string representation of a member.

        Members are represented by the member name in lowercase.
        
        Args:
            value:
                A member of the class.
        
        Returns:
            A string representing the member.
        """
        try:
            display = Dice(value).name.lower()
        except ValueError:
            display = 'Unknown'
        return display
    
    @classmethod
    def convert_display_name(cls, name):
        """Convert a string name into the corresponding class name.

        Strings are converted by transforming the string into uppercase
        and matching the result against all members.
        
        Args:
            name:
                The name to convert.
        
        Returns:
            The matching member.
        """
        try:
            converted_name = name.upper()
            value = Dice[converted_name]
        except KeyError:
            value = Dice.D0
        return value

class Damage:
    """Represents damage dealt from a dice roll.
    
    Attributes:
        num_dice: The number of dice rolled.
        die: The type of dice rolled.
        damage: The type of damage.
    
    Methods:
        average: Returns the average damage for the dice type.
    """
    def __init__(self, num_dice: int, die: Dice, damage: DamageType) -> None:
        """Initializes Damage.
        
        Args:
            num_dice: The number of dice rolled.
            die: The type of dice rolled.
            damage: The type of damage.
        """
        self.num_dice = num_dice
        self.die = die
        self.damage = damage
    
    def average(self) -> float:
        """Calculates the average damage value.
        
        Returns:
            The average value of the dice.
        """
        return self.num_dice * (self.die + 1) / 2

class WeaponType(Enum):
    """Defines an enumeration of weapon types.
    
    Members:
        CLUB
        DAGGER
        GREATCLUB
        HANDAXE
        JAVELIN
        LIGHT_HAMMER
        MACE
        QUARTERSTAFF
        QUARTERSTAFF2H
        SICKLE
        SPEAR
        LIGHT_CROSSBOW
        DART
        SHORTBOW
        SLING
        BATTLEAXE
        BATTLEAXE2H
        FLAIL
        GLAIVE
        GREATAXE
        GREATSWORD
        HALBERD
        LANCE
        LONGSWORD
        LONGSWORD2H
        MAUL
        MORNINGSTAR
        PIKE
        RAPIER
        SCIMITAR
        SHORTSWORD
        TRIDENT
        TRIDENT2H
        WAR_PICK
        WARHAMMER
        WARHAMMER2H
        WHIP
        BLOWGUN
        HAND_CROSSBOW
        HEAVY_CROSSBOW
        LONGBOW
        NET
    
    Methods:
        get_values: Return a list of string representations of the members.
        get_display_name: Get a formatted string representation of a member.
        convert_display_name: Convert a string representatino of a member into the member object.
    """
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
        """Return a list of string representations of the class' members.
        
        Returns:
            A list of string representations of the class' members.
        """
        values = []
        for name, _ in WeaponType.__members__.items():
            if name.endswith('2H'):
                values.append(name[:-2].title().replace('_', ' ') + ' (2 hands)')
            else:
                values.append(name.title().replace('_', ' '))
        return values
    
    @classmethod
    def get_display_name(cls, value):
        """Return a string representation of a member.

        Members are represented by the member name in titlecase.
        
        Args:
            value:
                A member of the class.
        
        Returns:
            A string representing the member.
        """
        try:
            name = WeaponType(value).name
            if name.endswith('2H'):
                name = name[:-2] + ' (2 hands)'
            display = name.title().replace('_', ' ')
        except ValueError:
            display = 'Unknown'
        return display
    
    @classmethod
    def convert_display_name(cls, name):
        """Convert a string name into the corresponding class name.

        Strings are converted by transforming the string into uppercase
        and matching the result against all members.
        
        Args:
            name:
                The name to convert.
        
        Returns:
            The matching member.
        """
        try:
            converted_name = name.replace(' (2 hands)', '2H').replace(' ', '_').upper()
            value = WeaponType[converted_name]
        except KeyError:
            value = WeaponType.CLUB
        return value

class Weapon:
    """Represents a weapon that deals damage.
    
    Attributes:
        weapon_type: The WeaponType of weapon.
        bonus: A bonus to the weapon's hit and attack.
        extra_damage: A list of Damage objects that are added to the weapon's damage.
    
    Properties
        base_damage_die: Return the Dice member used by the weapon_type attribute.
        base_damage_type: Return the DamageType member used by the weapon_type attribute.
    
    Methods:
        average_damage: Return the average damage of the weapon.
        average_critical_damage: Return the average damage of the weapon when a
            critical hit is made.
    """
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
    def __init__(self, weapon_type: WeaponType, bonus: int = 0, extra_damage: List[Damage] = None):
        """Initializes the Weapon.
        
        Parameters:
            weapon_type: The WeaponType of weapon.
            bonus: A bonus to the weapon's hit and attack.
            extra_damage: A list of Damage objects that are added to the weapon's damage.
        """
        if extra_damage is None:
            extra_damage = []
        self.weapon_type = weapon_type
        self.bonus = bonus
        self.extra_damage = extra_damage

    @property
    def base_damage_die(self) -> Dice:
        """Return the Dice member used by the weapon_type attribute."""
        return self._weapon_map[self.weapon_type].die

    @property
    def base_damage_type(self):
        """Return the DamageType member used by the weapon_type attribute."""
        return self._weapon_map[self.weapon_type].damage
    
    def average_damage(self):
        """Return the average damage of the weapon."""
        average = self._weapon_map[self.weapon_type].average()
        average += self.bonus
        for damage in self.extra_damage:
            average += damage.average()
        return average
    
    def average_critical_damage(self):
        """Return the average damage of the weapon when a critical hit is made."""
        average = 2 * self._weapon_map[self.weapon_type].average()
        average += self.bonus
        for damage in self.extra_damage:
            average += 2 * damage.average()
        return average

class WeaponAttack:
    """Represents an attack made by a weapon.
    
    Simulates attacking and damaging with a weapon. Calculates values relevant to D&D combat.
    
    Attributes:
        weapon: The Weapon used in the attack.
        level: The level of the player character.
        attack_stat: The player character's primary attack ability score.
        proficient: If the player character is proficient with the Weapon.
        damage_mod: An additional bonus to damage.
    
    Properties:
        proficiency_bonus: The player character's proficiency bonus.
        attack_mod: The modifier calculated from attack_stat.
        hit_bonus: The total bonus to hit an enemy.

    Methods:
        hit_chance: Calculate the chance to hit a given target AC.
        average_hit_damage: Calculate the average damage done on a hit.
        average_damage: Calculate the average damage done to a given target AC.
        critical_hit_damage: Calculate the damage done by a critical hit.
    """
    def __init__(self, weapon: Weapon, level: int, attack_stat: int, proficient: bool = True,
                 damage_mod: int = 0):
        """Initializes the WeaponAttack.
        
        Parameters:
            weapon: The Weapon used in the attack.
            level: The level of the player character.
            attack_stat: The player character's primary attack ability score.
            proficient: If the player character is proficient with the Weapon.
            damage_mod: An additional bonus to damage.
        """
        self.weapon = weapon
        self.level = level
        self.attack_stat = attack_stat
        self.proficient = proficient
        self.damage_mod = damage_mod
    
    @property
    def proficiency_bonus(self) -> int:
        """The player character's proficiency bonus.
        
        Calculated based on level. If level is not in the acceptable range (1-20 inclusive),
        return 2.
        """
        if 0 < self.level <= 4:
            return 2
        if 4 < self.level <= 8:
            return 3
        if 8 < self.level <= 12:
            return 4
        if 12 < self.level <= 16:
            return 5
        if 16 < self.level <= 20:
            return 6
        return 2
    
    @property
    def attack_mod(self) -> int:
        """The modifier calculated from attack_stat.
        
        Modifier is calculated as floor((attack_stat - 20) / 2)
        """
        return floor((self.attack_stat - 10) / 2)
    
    @property
    def hit_bonus(self) -> int:
        """The total bonus to hit an enemy.
        
        Total hit bonus is calculated using proficiency bonus, attack mod, and weapon bonus.
        """
        return ((self.proficiency_bonus if self.proficient else 0) + self.attack_mod +
                self.weapon.bonus)
    
    def hit_chance(self, target_ac: int):
        """Calculate the chance to hit a given target AC.
        
        Parameters:
            target_ac: The AC of the target of the attack.
        
        Returns:
            The chance to hit expressed as a value to be divided by 20.
        """
        return max(min(Dice.D20 - target_ac + self.hit_bonus + 1, 19), 1)
    
    def average_hit_damage(self) -> float:
        """Calculate the average damage by the attack on a hit.
        
        Returns:
            The calculated average damage.
        """
        return self.weapon.average_damage() + self.attack_mod + self.damage_mod
    
    def average_damage(self, target_ac: int) -> float:
        """Calculate the average damage done to a given target AC.

        Average damage takes into account hit chance and critical hits.

        Parameters:
            target_ac: The AC of the target of the attack.
        
        Returns:
            The calculated average damage.
        """
        return (max((self.hit_chance(target_ac) - 1), 1) / Dice.D20 * self.average_hit_damage() +
                1 / Dice.D20 * self.critical_hit_damage())
    
    def critical_hit_damage(self) -> float:
        """
        Calculate the average damage done by a critical hit.

        Critical hit damage is calulated by averaging dice, doubling, and adding modifiers.

        Returns:
            The calculated average damage of a critical hit.
        """
        return self.weapon.average_critical_damage() + self.attack_mod + self.damage_mod