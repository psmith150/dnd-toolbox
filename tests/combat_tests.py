import unittest
from toolbox.combat import Damage, WeaponType, Weapon, WeaponAttack, Dice, DamageType

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
    def setUp(self) -> None:
        weapon = Weapon(WeaponType.WARHAMMER)
        self.hammer_attack = WeaponAttack(weapon, 5, 18)
        weapon = Weapon(WeaponType.MACE, 1, [Damage(1, Dice.D6, DamageType.BLUDGEONING),])
        self.mace_attack = WeaponAttack(weapon, 5, 18)
    
    def test_hit_chance(self):
        weapon = Weapon(WeaponType.WARHAMMER)
        weapon_attack = WeaponAttack(weapon, 5, 18)
        self.assertEqual(weapon_attack.hit_chance(11), 17)
    
    def test_hit_chance_bonus(self):
        weapon = Weapon(WeaponType.MACE, bonus=1)
        weapon_attack = WeaponAttack(weapon, 5, 18)
        self.assertEqual(weapon_attack.hit_chance(11), 18)

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