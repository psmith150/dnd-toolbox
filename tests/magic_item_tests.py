#pylint: disable=C,R,W
#pylint: enable=F,E

"""Test the implementation of the magic_items.py module."""
from unittest import TestCase
from toolbox.magic_items import MagicItem, MagicItemDbInterface

class MagicItemDbInterfaceTestCase(TestCase):
    def test_get_magic_items(self):
        db = MagicItemDbInterface()
        items = db.get_magic_items()
        self.assertTrue(items)