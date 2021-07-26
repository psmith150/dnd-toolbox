from unittest import TestCase
from toolbox.common import Ability, AbilitySet, Skill, Tool

class SkillTestCase(TestCase):
    def testAbility(self):
        skill = Skill.ACROBATICS
        self.assertEqual(skill.ability(), Ability.DEXTERITY)

class ToolTestCase(TestCase):
    def testSkills(self):
        tool = Tool.ALCHEMIST
        self.assertTrue(Skill.ARCANA in tool.skills())

class AbilitySetTestCase(TestCase):
    def testGetAbility(self):
        abilities = AbilitySet(10, 11, 12, 13, 14, 15)
        self.assertEqual(abilities[Ability.CHARISMA], abilities.charisma)

    def testSetAbility(self):
        abilities = AbilitySet(10, 11, 12, 13, 14, 15)
        abilities[Ability.CHARISMA] = 17
        self.assertEqual(abilities.charisma, 17)