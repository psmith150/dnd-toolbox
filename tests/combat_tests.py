"""Test the implementation of the combat.py module."""
import unittest
from toolbox.combat import Damage, WeaponType, Weapon, WeaponAttack, Dice, DamageType

class DamageTypeTestCase(unittest.TestCase):
    def test_get_values(self):
        values = DamageType.get_values()
        self.assertEqual(len(values), len(list(DamageType)))
    
    def test_convert_display_name(self):
        val = DamageType(1)
        self.assertEqual(DamageType.convert_display_name(DamageType.get_display_name(val)), val)

class DiceTestCase(unittest.TestCase):
    def test_get_values(self):
        values = Dice.get_values()
        self.assertEqual(len(values), len(list(Dice)))
    
    def test_convert_display_name(self):
        val = Dice(1)
        self.assertEqual(Dice.convert_display_name(Dice.get_display_name(val)), val)

class DamageTestCase(unittest.TestCase):
    def test_average(self):
        damage = Damage(1, Dice.D6, DamageType.PIERCING)
        self.assertAlmostEqual(damage.average(), 3.5)

class WeaponTypeTestCase(unittest.TestCase):
    def test_get_values(self):
        values = WeaponType.get_values()
        self.assertEqual(len(values), len(list(WeaponType)))
    
    def test_convert_display_name(self):
        val = WeaponType(1)
        self.assertEqual(WeaponType.convert_display_name(WeaponType.get_display_name(val)), val)

class WeaponTestCase(unittest.TestCase):
    def test_average_damage(self):
        weapon = Weapon(WeaponType.WARHAMMER)
        self.assertAlmostEqual(weapon.average_damage(), 4.5)
    
    def test_average_damage_bonus(self):
        weapon = Weapon(WeaponType.MACE, bonus=1)
        self.assertAlmostEqual(weapon.average_damage(), 4.5)
    
    def test_average_damage_extra_damage(self):
        weapon = Weapon(WeaponType.MACE, extra_damage=[Damage(1, Dice.D6, DamageType.BLUDGEONING),])
        self.assertAlmostEqual(weapon.average_damage(), 7)
    
    def test_average_damage_bonus_and_extra_damage(self):
        weapon = Weapon(WeaponType.MACE, bonus=1, extra_damage=[Damage(1, Dice.D6, DamageType.BLUDGEONING),])
        self.assertAlmostEqual(weapon.average_damage(), 8)

class AttackTestCase(unittest.TestCase):    
    def test_hit_chance(self):
        weapon = Weapon(WeaponType.WARHAMMER)
        weapon_attack = WeaponAttack(weapon, 5, 18)
        self.assertEqual(weapon_attack.hit_chance(11), 17)
    
    def test_hit_chance_bonus(self):
        weapon = Weapon(WeaponType.MACE, bonus=1)
        weapon_attack = WeaponAttack(weapon, 5, 18)
        self.assertEqual(weapon_attack.hit_chance(11), 18)

    def test_average_hit_damage(self):
        weapon = Weapon(WeaponType.WARHAMMER)
        weapon_attack = WeaponAttack(weapon, 5, 18)
        self.assertAlmostEqual(weapon_attack.average_hit_damage(), 8.5)
    
    def test_average_hit_damage_bonus(self):
        weapon = Weapon(WeaponType.MACE, bonus=1)
        weapon_attack = WeaponAttack(weapon, 5, 18)
        self.assertAlmostEqual(weapon_attack.average_hit_damage(), 8.5)
    
    def test_average_hit_damage_extra_damage(self):
        weapon = Weapon(WeaponType.MACE, extra_damage=[Damage(1, Dice.D6, DamageType.BLUDGEONING),])
        weapon_attack = WeaponAttack(weapon, 5, 18)
        self.assertAlmostEqual(weapon_attack.average_hit_damage(), 11.0)
    
    def test_average_hit_damage_bonus_and_extra_damage(self):
        weapon = Weapon(WeaponType.MACE, bonus=1, extra_damage=[Damage(1, Dice.D6, DamageType.BLUDGEONING),])
        weapon_attack = WeaponAttack(weapon, 5, 18)
        self.assertAlmostEqual(weapon_attack.average_hit_damage(), 12.0)
    
    def test_average_damage(self):
        weapon = Weapon(WeaponType.WARHAMMER)
        weapon_attack = WeaponAttack(weapon, 5, 18)
        self.assertAlmostEqual(weapon_attack.average_damage(11), 7.45)
    
    def test_average_damage_bonus(self):
        weapon = Weapon(WeaponType.MACE, bonus=1)
        weapon_attack = WeaponAttack(weapon, 5, 18)
        self.assertAlmostEqual(weapon_attack.average_damage(11), 7.825)
    
    def test_average_damage_extra_damage(self):
        weapon = Weapon(WeaponType.MACE, extra_damage=[Damage(1, Dice.D6, DamageType.BLUDGEONING),])
        weapon_attack = WeaponAttack(weapon, 5, 18)
        self.assertAlmostEqual(weapon_attack.average_damage(11), 9.7)
    
    def test_average_damage_bonus_and_extra_damage(self):
        weapon = Weapon(WeaponType.MACE, bonus=1, extra_damage=[Damage(1, Dice.D6, DamageType.BLUDGEONING),])
        weapon_attack = WeaponAttack(weapon, 5, 18)
        self.assertAlmostEqual(weapon_attack.average_damage(11), 11.15)
    
    def test_critical_hit_damage(self):
        weapon = Weapon(WeaponType.WARHAMMER)
        weapon_attack = WeaponAttack(weapon, 5, 18)
        self.assertAlmostEqual(weapon_attack.critical_hit_damage(), 13.0)
    
    def test_critical_hit_damage_bonus(self):
        weapon = Weapon(WeaponType.MACE, bonus=1)
        weapon_attack = WeaponAttack(weapon, 5, 18)
        self.assertAlmostEqual(weapon_attack.critical_hit_damage(), 12.0)
    
    def test_critical_hit_damage_extra_damage(self):
        weapon = Weapon(WeaponType.MACE, extra_damage=[Damage(1, Dice.D6, DamageType.BLUDGEONING),])
        weapon_attack = WeaponAttack(weapon, 5, 18)
        self.assertAlmostEqual(weapon_attack.critical_hit_damage(), 18.0)
    
    def test_critical_hit_damage_bonus_and_extra_damage(self):
        weapon = Weapon(WeaponType.MACE, bonus=1, extra_damage=[Damage(1, Dice.D6, DamageType.BLUDGEONING),])
        weapon_attack = WeaponAttack(weapon, 5, 18)
        self.assertAlmostEqual(weapon_attack.critical_hit_damage(), 19.0)